import test from 'node:test';
import assert from 'node:assert/strict';
import {
  resetDatabase,
  seedBaselineUsersAndRooms,
  insertConfirmedBooking,
  SEED_IDS,
  SEED_PASSWORD,
  withTestClient,
} from './helpers/db.js';
import { startTestServer } from './helpers/http.js';

test('S-1-2 拒絕重疊時段並提示衝突', async () => {
  await resetDatabase();
  await seedBaselineUsersAndRooms();
  await insertConfirmedBooking({
    startsAt: '2026-07-31T14:00:00+08:00',
    endsAt: '2026-07-31T15:00:00+08:00',
  });

  const server = await startTestServer();
  try {
    const login = await server.request('POST', '/api/auth/login', {
      body: { username: 'alice', password: SEED_PASSWORD },
    });
    assert.equal(login.status, 200);

    const before = await withTestClient(async (client) => {
      const r = await client.query(
        `SELECT count(*)::int AS n FROM bookings WHERE status = 'confirmed'`,
      );
      return r.rows[0].n;
    });

    const booking = await server.request('POST', '/api/bookings', {
      body: {
        room_id: SEED_IDS.roomActive,
        purpose: '衝突會議',
        attendee_count: 3,
        needs_projector: false,
        needs_video_conference: false,
        starts_at: '2026-07-31T14:30:00+08:00',
        ends_at: '2026-07-31T15:30:00+08:00',
      },
    });

    assert.equal(booking.status, 409);
    assert.equal(booking.body.error.code, 'BOOKING_CONFLICT');
    assert.match(String(booking.body.error.message), /衝突|conflict/i);

    const after = await withTestClient(async (client) => {
      const r = await client.query(
        `SELECT count(*)::int AS n FROM bookings WHERE status = 'confirmed'`,
      );
      return r.rows[0].n;
    });
    assert.equal(after, before);
  } finally {
    await server.close();
  }
});
