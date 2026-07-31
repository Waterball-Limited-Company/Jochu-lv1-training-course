import { query } from '../db/pool.js';

async function findByUsername(username) {
  const result = await query(
    `SELECT id, username, password_hash, display_name, role, created_at
       FROM users
      WHERE username = $1`,
    [username],
  );
  return result.rows[0] ?? null;
}

export const userModel = { findByUsername };
