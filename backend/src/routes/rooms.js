import { Router } from 'express';
import { requireAuth } from '../middleware/auth.js';
import { requireRole } from '../middleware/requireRole.js';
import { sendError } from '../lib/errors.js';
import { parseInstant } from '../lib/time.js';
import { roomModel } from '../models/room.js';
import { maintenanceModel } from '../models/maintenance.js';

const router = Router();
const UUID_PATTERN =
  /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const adminOnly = [requireAuth, requireRole('facility_admin')];

router.get('/', requireAuth, async (_req, res, next) => {
  try {
    return res.status(200).json({ rooms: await roomModel.listAll() });
  } catch (error) {
    return next(error);
  }
});

router.post('/', ...adminOnly, async (req, res, next) => {
  const body = req.body ?? {};
  if (
    typeof body.name !== 'string' ||
    !body.name.trim() ||
    typeof body.floor !== 'string' ||
    !body.floor.trim() ||
    !Number.isInteger(body.capacity) ||
    body.capacity < 1 ||
    typeof body.has_projector !== 'boolean' ||
    typeof body.has_video_conference !== 'boolean'
  ) {
    return sendError(res, 400, 'VALIDATION_ERROR', 'Room fields are missing or invalid');
  }
  try {
    return res.status(201).json(await roomModel.create(body));
  } catch (error) {
    return next(error);
  }
});

router.patch('/:roomId', ...adminOnly, async (req, res, next) => {
  if (!UUID_PATTERN.test(req.params.roomId)) {
    return sendError(res, 404, 'ROOM_NOT_FOUND', 'Room was not found');
  }
  if (
    !req.body ||
    Object.keys(req.body).length !== 1 ||
    req.body.is_active !== false
  ) {
    return sendError(res, 400, 'VALIDATION_ERROR', 'is_active must be false', {
      details: [{ field: 'is_active', reason: 'only deactivation is supported' }],
    });
  }
  try {
    const room = await roomModel.deactivate(req.params.roomId);
    if (!room) return sendError(res, 404, 'ROOM_NOT_FOUND', 'Room was not found');
    return res.status(200).json(room);
  } catch (error) {
    return next(error);
  }
});

router.post(
  '/:roomId/maintenance-windows',
  ...adminOnly,
  async (req, res, next) => {
    if (!UUID_PATTERN.test(req.params.roomId)) {
      return sendError(res, 404, 'ROOM_NOT_FOUND', 'Room was not found');
    }
    const startsAt = parseInstant(req.body?.starts_at);
    const endsAt = parseInstant(req.body?.ends_at);
    if (!startsAt || !endsAt || endsAt <= startsAt) {
      return sendError(
        res,
        400,
        'VALIDATION_ERROR',
        'ends_at must be later than starts_at',
        { details: [{ field: 'ends_at', reason: 'must_be_after_starts_at' }] },
      );
    }
    if (req.body.note !== undefined && typeof req.body.note !== 'string') {
      return sendError(res, 400, 'VALIDATION_ERROR', 'note must be a string');
    }
    try {
      const maintenance = await maintenanceModel.create({
        roomId: req.params.roomId,
        userId: req.user.id,
        startsAt,
        endsAt,
        note: req.body.note,
      });
      if (!maintenance) {
        return sendError(res, 404, 'ROOM_NOT_FOUND', 'Room was not found');
      }
      return res.status(201).json(maintenance);
    } catch (error) {
      return next(error);
    }
  },
);

export default router;
