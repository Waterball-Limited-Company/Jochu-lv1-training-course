import { randomUUID } from 'node:crypto';
import { query } from '../db/pool.js';

async function create({ roomId, userId, startsAt, endsAt, note }) {
  const result = await query(
    `INSERT INTO maintenance_windows (
       id, room_id, starts_at, ends_at, note, created_by
     )
     SELECT $1, r.id, $3::timestamptz, $4::timestamptz, $5, $6
       FROM rooms r
      WHERE r.id = $2
     RETURNING id, room_id, starts_at, ends_at, note, created_by, created_at`,
    [randomUUID(), roomId, startsAt, endsAt, note ?? null, userId],
  );
  return result.rows[0] ?? null;
}

export const maintenanceModel = { create };
