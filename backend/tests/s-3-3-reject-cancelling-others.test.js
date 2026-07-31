import test from 'node:test';
import assert from 'node:assert/strict';
import {
  resetDatabase, seedBaselineUsersAndRooms, insertConfirmedBooking,
  SEED_IDS, SEED_PASSWORD, withTestClient,
} from './helpers/db.js';
import { startTestServer } from './helpers/http.js';

test('S-3-3 不得取消他人預約', async () => {
  await resetDatabase();
  await seedBaselineUsersAndRooms();
  const bookingId = await insertConfirmedBooking({
    userId: SEED_IDS.bob,
    startsAt: '2026-07-31T14:00:00+08:00',
    endsAt: '2026-07-31T15:00:00+08:00',
  });
  const before = await withTestClient(async (client) =>
    (await client.query('SELECT updated_at FROM bookings WHERE id = $1', [bookingId])).rows[0]);
  const server = await startTestServer();
  try {
    await server.request('POST', '/api/auth/login', {
      body: { username: 'alice', password: SEED_PASSWORD },
    });
    const res = await server.request('POST', `/api/bookings/${bookingId}/cancel`);
    assert.equal(res.status, 403);
    assert.equal(res.body.error.code, 'FORBIDDEN');
    const after = await withTestClient(async (client) =>
      (await client.query('SELECT status, updated_at FROM bookings WHERE id = $1', [bookingId])).rows[0]);
    assert.equal(after.status, 'confirmed');
    assert.equal(after.updated_at.getTime(), before.updated_at.getTime());
  } finally {
    await server.close();
  }
});
