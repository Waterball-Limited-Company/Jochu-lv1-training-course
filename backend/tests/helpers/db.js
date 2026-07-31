import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import pg from 'pg';
import bcrypt from 'bcrypt';
import { randomUUID } from 'node:crypto';

const { Client } = pg;

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const schemaPath = path.resolve(__dirname, '../../db/schema.sql');

export const TEST_DATABASE_URL =
  process.env.TEST_DATABASE_URL ??
  'postgres://meeting:meeting@127.0.0.1:5432/meeting_room_test';

export const SEED_PASSWORD = 'training-password';

export const SEED_IDS = {
  alice: '11111111-1111-4111-8111-111111111111',
  bob: '22222222-2222-4222-8222-222222222222',
  admin: '33333333-3333-4333-8333-333333333333',
  roomActive: 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
  roomInactive: 'bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb',
};

export async function createAdminClient() {
  const url = new URL(TEST_DATABASE_URL);
  const dbName = url.pathname.replace(/^\//, '');
  url.pathname = '/postgres';
  const client = new Client({ connectionString: url.toString() });
  await client.connect();
  const exists = await client.query('SELECT 1 FROM pg_database WHERE datname = $1', [
    dbName,
  ]);
  if (exists.rowCount === 0) {
    await client.query(`CREATE DATABASE "${dbName}"`);
  }
  await client.end();
}

export async function withTestClient(fn) {
  const client = new Client({ connectionString: TEST_DATABASE_URL });
  await client.connect();
  try {
    return await fn(client);
  } finally {
    await client.end();
  }
}

export async function applySchema(client) {
  const sql = await fs.readFile(schemaPath, 'utf8');
  await client.query(sql);
}

export async function resetDatabase() {
  await createAdminClient();
  await withTestClient(async (client) => {
    await client.query(`
      DROP TABLE IF EXISTS maintenance_windows CASCADE;
      DROP TABLE IF EXISTS bookings CASCADE;
      DROP TABLE IF EXISTS holidays CASCADE;
      DROP TABLE IF EXISTS rooms CASCADE;
      DROP TABLE IF EXISTS users CASCADE;
      DROP TABLE IF EXISTS session CASCADE;
    `);
    await applySchema(client);
  });
}

export async function seedBaselineUsersAndRooms() {
  const passwordHash = await bcrypt.hash(SEED_PASSWORD, 10);
  await withTestClient(async (client) => {
    await client.query(
      `INSERT INTO users (id, username, password_hash, display_name, role)
       VALUES
         ($1, 'alice', $4, 'Alice Employee', 'employee'),
         ($2, 'bob', $4, 'Bob Manager', 'manager'),
         ($3, 'admin', $4, 'Facility Admin', 'facility_admin')`,
      [SEED_IDS.alice, SEED_IDS.bob, SEED_IDS.admin, passwordHash],
    );
    await client.query(
      `INSERT INTO rooms (
         id, name, floor, capacity, has_projector, has_video_conference, is_active
       ) VALUES
         ($1, 'Sunrise', '3F', 8, true, true, true),
         ($2, 'Moonlight', '5F', 12, false, true, false)`,
      [SEED_IDS.roomActive, SEED_IDS.roomInactive],
    );
  });
}

export async function insertConfirmedBooking({
  id = randomUUID(),
  roomId = SEED_IDS.roomActive,
  userId = SEED_IDS.bob,
  purpose = '既有會議',
  attendeeCount = 4,
  needsProjector = false,
  needsVideoConference = false,
  startsAt,
  endsAt,
}) {
  await withTestClient(async (client) => {
    await client.query(
      `INSERT INTO bookings (
         id, room_id, user_id, purpose, attendee_count,
         needs_projector, needs_video_conference, starts_at, ends_at, status
       ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8::timestamptz,$9::timestamptz,'confirmed')`,
      [
        id,
        roomId,
        userId,
        purpose,
        attendeeCount,
        needsProjector,
        needsVideoConference,
        startsAt,
        endsAt,
      ],
    );
  });
  return id;
}

export async function insertHoliday(holidayDate, name = 'Seed Holiday') {
  await withTestClient(async (client) => {
    await client.query(
      `INSERT INTO holidays (holiday_date, name) VALUES ($1::date, $2)
       ON CONFLICT (holiday_date) DO NOTHING`,
      [holidayDate, name],
    );
  });
}

export async function assertCanConnect() {
  await createAdminClient();
  await withTestClient(async (client) => {
    const result = await client.query('SELECT 1 AS ok');
    if (result.rows[0].ok !== 1) {
      throw new Error('unexpected connectivity result');
    }
  });
}

export { randomUUID };
