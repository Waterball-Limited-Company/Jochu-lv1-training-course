import test from 'node:test';
import assert from 'node:assert/strict';
import {
  resetDatabase,
  seedBaselineUsersAndRooms,
  SEED_IDS,
  withTestClient,
} from './helpers/db.js';
import { startTestServer } from './helpers/http.js';

test('S-1-3 未登入不得建立預約', async () => {
  await resetDatabase();
  await seedBaselineUsersAndRooms();

  const server = await startTestServer();
  try {
    const booking = await server.request('POST', '/api/bookings', {
      body: {
        room_id: SEED_IDS.roomActive,
        purpose: '未登入嘗試',
        attendee_count: 2,
        needs_projector: false,
        needs_video_conference: false,
        starts_at: '2026-07-31T10:00:00+08:00',
        ends_at: '2026-07-31T11:00:00+08:00',
      },
    });

    assert.equal(booking.status, 401);
    assert.equal(booking.body.error.code, 'UNAUTHENTICATED');

    await withTestClient(async (client) => {
      const r = await client.query('SELECT count(*)::int AS n FROM bookings');
      assert.equal(r.rows[0].n, 0);
    });
  } finally {
    await server.close();
  }
});
