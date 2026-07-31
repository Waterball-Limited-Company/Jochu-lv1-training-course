import test from 'node:test';
import assert from 'node:assert/strict';
import {
  resetDatabase, seedBaselineUsersAndRooms, SEED_IDS, SEED_PASSWORD, withTestClient,
} from './helpers/db.js';
import { startTestServer } from './helpers/http.js';

test('S-4-2 維護時段內拒絕新預約', async () => {
  await resetDatabase();
  await seedBaselineUsersAndRooms();
  const admin = await startTestServer();
  const employee = await startTestServer();
  try {
    await admin.request('POST', '/api/auth/login', {
      body: { username: 'admin', password: SEED_PASSWORD },
    });
    const maintenance = await admin.request(
      'POST', `/api/rooms/${SEED_IDS.roomActive}/maintenance-windows`,
      { body: {
        starts_at: '2026-07-31T10:00:00+08:00',
        ends_at: '2026-07-31T12:00:00+08:00',
        note: '空調維修',
      } },
    );
    assert.equal(maintenance.status, 201);
    assert.equal(maintenance.body.created_by, SEED_IDS.admin);

    await employee.request('POST', '/api/auth/login', {
      body: { username: 'alice', password: SEED_PASSWORD },
    });
    const booking = await employee.request('POST', '/api/bookings', {
      body: {
        room_id: SEED_IDS.roomActive, purpose: '衝突會議', attendee_count: 2,
        needs_projector: false, needs_video_conference: false,
        starts_at: '2026-07-31T10:30:00+08:00',
        ends_at: '2026-07-31T11:30:00+08:00',
      },
    });
    assert.equal(booking.status, 409);
    assert.equal(booking.body.error.code, 'MAINTENANCE_CONFLICT');
    const count = await withTestClient(async (client) =>
      (await client.query('SELECT count(*)::int AS n FROM bookings')).rows[0].n);
    assert.equal(count, 0);
  } finally {
    await admin.close();
    await employee.close();
  }
});
