import { Router } from 'express';
import { requireAuth } from '../middleware/auth.js';
import { sendError } from '../lib/errors.js';
import {
  getTaipeiDayBounds,
  getTaipeiParts,
  getTaipeiTimeZone,
  parseInstant,
} from '../lib/time.js';
import { obeysBookingRules } from '../lib/booking-rules.js';
import { bookingModel, BookingModelError } from '../models/booking.js';

const router = Router();
const UUID_PATTERN =
  /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

function validateInput(body) {
  if (
    !body ||
    typeof body.room_id !== 'string' ||
    !UUID_PATTERN.test(body.room_id) ||
    typeof body.purpose !== 'string' ||
    !body.purpose.trim() ||
    !Number.isInteger(body.attendee_count) ||
    body.attendee_count < 1 ||
    typeof body.needs_projector !== 'boolean' ||
    typeof body.needs_video_conference !== 'boolean'
  ) {
    return { error: 'Required booking fields are missing or invalid' };
  }

  const startsAt = parseInstant(body.starts_at);
  const endsAt = parseInstant(body.ends_at);
  if (!startsAt || !endsAt || endsAt <= startsAt) {
    return { error: 'Booking start and end times are invalid' };
  }
  return { startsAt, endsAt };
}

const MODEL_ERROR_MAP = {
  ROOM_NOT_FOUND: [404, 'Room was not found'],
  BOOKING_CONFLICT: [
    409,
    'The room already has a confirmed booking conflict in this time range',
  ],
  MAINTENANCE_CONFLICT: [
    409,
    'The room is unavailable during a maintenance window',
  ],
  BOOKING_RULE_VIOLATION: [
    400,
    'The booking violates room availability or capacity rules',
  ],
};

router.get('/mine', requireAuth, async (req, res, next) => {
  try {
    return res.status(200).json({
      bookings: await bookingModel.listMine(req.user.id),
    });
  } catch (error) {
    return next(error);
  }
});

router.post('/:bookingId/cancel', requireAuth, async (req, res, next) => {
  if (!UUID_PATTERN.test(req.params.bookingId)) {
    return sendError(res, 404, 'BOOKING_NOT_FOUND', 'Booking was not found');
  }
  try {
    const booking = await bookingModel.cancel({
      bookingId: req.params.bookingId,
      userId: req.user.id,
    });
    return res.status(200).json(booking);
  } catch (error) {
    if (!(error instanceof BookingModelError)) return next(error);
    if (error.code === 'BOOKING_NOT_FOUND') {
      return sendError(res, 404, error.code, 'Booking was not found');
    }
    if (error.code === 'FORBIDDEN') {
      return sendError(res, 403, error.code, "You cannot cancel another user's booking");
    }
    if (error.code === 'BOOKING_NOT_CANCELLABLE') {
      return sendError(
        res,
        409,
        error.code,
        'Booking is already cancelled or has ended',
      );
    }
    return next(error);
  }
});

router.get('/', requireAuth, async (req, res, next) => {
  const bounds = getTaipeiDayBounds(req.query.date);
  if (!bounds) {
    return sendError(
      res,
      400,
      'VALIDATION_ERROR',
      'date must use YYYY-MM-DD',
      { details: [{ field: 'date', reason: 'invalid_date' }] },
    );
  }

  const roomId = req.query.roomId;
  if (roomId !== undefined && (typeof roomId !== 'string' || !UUID_PATTERN.test(roomId))) {
    return sendError(res, 400, 'VALIDATION_ERROR', 'roomId must be a UUID', {
      details: [{ field: 'roomId', reason: 'invalid_uuid' }],
    });
  }

  try {
    if (roomId && !(await bookingModel.roomExists(roomId))) {
      return sendError(res, 404, 'ROOM_NOT_FOUND', 'Room was not found');
    }
    const bookings = await bookingModel.listConfirmed({
      start: bounds.start,
      end: bounds.end,
      roomId,
    });
    return res.status(200).json({
      date: req.query.date,
      timezone: getTaipeiTimeZone(),
      bookings,
    });
  } catch (error) {
    return next(error);
  }
});

router.post('/', requireAuth, async (req, res, next) => {
  const validated = validateInput(req.body);
  if (validated.error) {
    return sendError(res, 400, 'VALIDATION_ERROR', validated.error);
  }
  if (!obeysBookingRules(validated.startsAt, validated.endsAt)) {
    return sendError(
      res,
      400,
      'BOOKING_RULE_VIOLATION',
      'Booking violates the Asia/Taipei business-day rules',
    );
  }

  try {
    const booking = await bookingModel.createConfirmed({
      userId: req.user.id,
      input: {
        ...req.body,
        starts_at: validated.startsAt,
        ends_at: validated.endsAt,
      },
      taipeiDate: getTaipeiParts(validated.startsAt).date,
    });
    return res.status(201).json(booking);
  } catch (error) {
    if (!(error instanceof BookingModelError)) return next(error);
    const mapped = MODEL_ERROR_MAP[error.code] ?? MODEL_ERROR_MAP.BOOKING_RULE_VIOLATION;
    return sendError(res, mapped[0], error.code, mapped[1]);
  }
});

export default router;
