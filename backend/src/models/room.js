import { query } from '../db/pool.js';
import { randomUUID } from 'node:crypto';

async function listAll() {
  const result = await query(
    `SELECT id, name, floor, capacity, has_projector,
            has_video_conference, is_active, created_at, updated_at
       FROM rooms
      ORDER BY floor, name`,
  );
  return result.rows;
}

async function create(input) {
  const result = await query(
    `INSERT INTO rooms (
       id, name, floor, capacity, has_projector, has_video_conference, is_active
     ) VALUES ($1, $2, $3, $4, $5, $6, true)
     RETURNING id, name, floor, capacity, has_projector,
               has_video_conference, is_active, created_at, updated_at`,
    [
      randomUUID(),
      input.name.trim(),
      input.floor.trim(),
      input.capacity,
      input.has_projector,
      input.has_video_conference,
    ],
  );
  return result.rows[0];
}

async function deactivate(roomId) {
  const result = await query(
    `UPDATE rooms
        SET is_active = false, updated_at = now()
      WHERE id = $1
      RETURNING id, name, floor, capacity, has_projector,
                has_video_conference, is_active, created_at, updated_at`,
    [roomId],
  );
  return result.rows[0] ?? null;
}

export const roomModel = { listAll, create, deactivate };
