import { Router } from 'express';
import { pool } from '../db/pool.js';
import { requireAuth } from '../middleware/auth.js';
import {
  getTaipeiDayBounds,
  getTaipeiParts,
  getTaipeiTimeZone,
} from '../lib/time.js';

const router = Router();

router.get('/today', requireAuth, async (_req, res, next) => {
  const now = new Date();
  const taipei = getTaipeiParts(now);
  const bounds = getTaipeiDayBounds(taipei.date);

  try {
    const holiday = await pool.query(
      'SELECT 1 FROM holidays WHERE holiday_date = $1::date',
      [taipei.date],
    );
    const isBusinessDay =
      !['Sat', 'Sun'].includes(taipei.weekday) && holiday.rowCount === 0;
    const businessMinutes = isBusinessDay ? 720 : 0;
    const result = await pool.query(
      `SELECT r.id AS room_id, r.name AS room_name, r.is_active,
              COUNT(b.id)::integer AS confirmed_booking_count,
              CASE WHEN $5::boolean THEN
                COALESCE(ROUND(SUM(
                  CASE WHEN b.id IS NULL THEN 0 ELSE GREATEST(
                    EXTRACT(EPOCH FROM (
                      LEAST(b.ends_at, $4::timestamptz) -
                      GREATEST(b.starts_at, $3::timestamptz)
                    )) / 60,
                    0
                  ) END
                )), 0)::integer
              ELSE 0 END AS booked_minutes
         FROM rooms r
         LEFT JOIN bookings b
           ON b.room_id = r.id
          AND b.status = 'confirmed'
          AND b.starts_at < $2::timestamptz
          AND b.ends_at > $1::timestamptz
        GROUP BY r.id, r.name, r.is_active
        ORDER BY r.name`,
      [
        bounds.start,
        bounds.end,
        bounds.businessStart,
        bounds.businessEnd,
        isBusinessDay,
      ],
    );

    return res.status(200).json({
      date: taipei.date,
      timezone: getTaipeiTimeZone(),
      rooms: result.rows.map((room) => ({
        ...room,
        business_minutes: businessMinutes,
        busy_ratio:
          businessMinutes > 0 ? room.booked_minutes / businessMinutes : 0,
      })),
    });
  } catch (error) {
    return next(error);
  }
});

export default router;
