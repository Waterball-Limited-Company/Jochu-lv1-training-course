import { randomUUID } from 'node:crypto';
import { pool } from '../db/pool.js';

export class BookingModelError extends Error {
  constructor(code) {
    super(code);
    this.code = code;
  }
}

async function createConfirmed({ userId, input, taipeiDate }) {
  const client = await pool.connect();
  try {
    await client.query('BEGIN');

    const roomResult = await client.query(
      `SELECT id, capacity, is_active
         FROM rooms
        WHERE id = $1
        FOR UPDATE`,
      [input.room_id],
    );
    const room = roomResult.rows[0];
    if (!room) throw new BookingModelError('ROOM_NOT_FOUND');
    if (!room.is_active || input.attendee_count > room.capacity) {
      throw new BookingModelError('BOOKING_RULE_VIOLATION');
    }

    const holiday = await client.query(
      'SELECT 1 FROM holidays WHERE holiday_date = $1::date',
      [taipeiDate],
    );
    if (holiday.rowCount > 0) throw new BookingModelError('BOOKING_RULE_VIOLATION');

    const maintenance = await client.query(
      `SELECT 1
         FROM maintenance_windows
        WHERE room_id = $1
          AND tstzrange(starts_at, ends_at, '[)') &&
              tstzrange($2::timestamptz, $3::timestamptz, '[)')
        LIMIT 1`,
      [input.room_id, input.starts_at, input.ends_at],
    );
    if (maintenance.rowCount > 0) throw new BookingModelError('MAINTENANCE_CONFLICT');

    const overlap = await client.query(
      `SELECT 1
         FROM bookings
        WHERE room_id = $1
          AND status = 'confirmed'
          AND tstzrange(starts_at, ends_at, '[)') &&
              tstzrange($2::timestamptz, $3::timestamptz, '[)')
        LIMIT 1`,
      [input.room_id, input.starts_at, input.ends_at],
    );
    if (overlap.rowCount > 0) throw new BookingModelError('BOOKING_CONFLICT');

    const result = await client.query(
      `INSERT INTO bookings (
         id, room_id, user_id, purpose, attendee_count,
         needs_projector, needs_video_conference, starts_at, ends_at, status
       ) VALUES (
         $1, $2, $3, $4, $5, $6, $7, $8::timestamptz, $9::timestamptz, 'confirmed'
       )
       RETURNING id, room_id, user_id, purpose, attendee_count,
                 needs_projector, needs_video_conference, starts_at, ends_at,
                 status, created_at, updated_at`,
      [
        randomUUID(),
        input.room_id,
        userId,
        input.purpose.trim(),
        input.attendee_count,
        input.needs_projector,
        input.needs_video_conference,
        input.starts_at,
        input.ends_at,
      ],
    );
    await client.query('COMMIT');
    return result.rows[0];
  } catch (error) {
    await client.query('ROLLBACK');
    if (error.code === '23P01') throw new BookingModelError('BOOKING_CONFLICT');
    throw error;
  } finally {
    client.release();
  }
}

async function listConfirmed({ start, end, roomId }) {
  const values = [start, end];
  const roomFilter = roomId ? `AND b.room_id = $${values.push(roomId)}` : '';
  const result = await pool.query(
    `SELECT b.id, b.room_id,
            json_build_object('name', r.name, 'floor', r.floor) AS room,
            b.user_id,
            json_build_object('display_name', u.display_name) AS booked_by,
            b.purpose, b.attendee_count, b.needs_projector,
            b.needs_video_conference, b.starts_at, b.ends_at,
            b.status, b.created_at, b.updated_at
       FROM bookings b
       JOIN rooms r ON r.id = b.room_id
       JOIN users u ON u.id = b.user_id
      WHERE b.status = 'confirmed'
        AND b.starts_at >= $1
        AND b.starts_at < $2
        ${roomFilter}
      ORDER BY b.starts_at, r.name`,
    values,
  );
  return result.rows;
}

async function listMine(userId) {
  const result = await pool.query(
    `SELECT b.id, b.room_id,
            json_build_object('name', r.name, 'floor', r.floor) AS room,
            b.user_id, b.purpose, b.attendee_count, b.needs_projector,
            b.needs_video_conference, b.starts_at, b.ends_at, b.status,
            (b.status = 'confirmed' AND b.ends_at > now()) AS is_cancellable,
            b.created_at, b.updated_at
       FROM bookings b
       JOIN rooms r ON r.id = b.room_id
      WHERE b.user_id = $1
        AND b.status IN ('confirmed', 'cancelled')
      ORDER BY b.starts_at DESC`,
    [userId],
  );
  return result.rows;
}

async function cancel({ bookingId, userId }) {
  const client = await pool.connect();
  try {
    await client.query('BEGIN');
    const found = await client.query(
      `SELECT id, room_id, user_id, purpose, attendee_count,
              needs_projector, needs_video_conference, starts_at, ends_at,
              status, created_at, updated_at
         FROM bookings
        WHERE id = $1
        FOR UPDATE`,
      [bookingId],
    );
    const booking = found.rows[0];
    if (!booking) throw new BookingModelError('BOOKING_NOT_FOUND');
    if (booking.user_id !== userId) throw new BookingModelError('FORBIDDEN');
    const result = await client.query(
      `UPDATE bookings
          SET status = 'cancelled', updated_at = now()
        WHERE id = $1
          AND status = 'confirmed'
          AND ends_at > now()
        RETURNING id, room_id, user_id, purpose, attendee_count,
                  needs_projector, needs_video_conference, starts_at, ends_at,
                  status, created_at, updated_at`,
      [bookingId],
    );
    if (result.rowCount === 0) {
      throw new BookingModelError('BOOKING_NOT_CANCELLABLE');
    }
    await client.query('COMMIT');
    return result.rows[0];
  } catch (error) {
    await client.query('ROLLBACK');
    throw error;
  } finally {
    client.release();
  }
}

async function roomExists(roomId) {
  const result = await pool.query('SELECT 1 FROM rooms WHERE id = $1', [roomId]);
  return result.rowCount > 0;
}

export const bookingModel = {
  createConfirmed,
  listConfirmed,
  listMine,
  cancel,
  roomExists,
};
