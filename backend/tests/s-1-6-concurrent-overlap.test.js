import test from 'node:test';
import assert from 'node:assert/strict';
import {
  resetDatabase,
  seedBaselineUsersAndRooms,
  SEED_IDS,
  SEED_PASSWORD,
  withTestClient,
} from './helpers/db.js';
import { startTestServer } from './helpers/http.js';

async function loginAs(server, username) {
  const login = await server.request('POST', '/api/auth/login', {
    body: { username, password: SEED_PASSWORD },
  });
  assert.equal(login.status, 200);
  return login;
}

test('S-1-6 併發重疊預約最多一筆確認', async () => {
  await resetDatabase();
  await seedBaselineUsersAndRooms();

  const aliceServer = await startTestServer();
  const bobServer = await startTestServer();
  try {
    await loginAs(aliceServer, 'alice');
    await loginAs(bobServer, 'bob');

    const payloadAlice = {
      room_id: SEED_IDS.roomActive,
      purpose: 'Alice 併發',
      attendee_count: 2,
      needs_projector: false,
      needs_video_conference: false,
      starts_at: '2026-07-31T16:00:00+08:00',
      ends_at: '2026-07-31T17:00:00+08:00',
    };
    const payloadBob = {
      ...payloadAlice,
      purpose: 'Bob 併發',
      starts_at: '2026-07-31T16:30:00+08:00',
      ends_at: '2026-07-31T17:30:00+08:00',
    };

    const [aliceRes, bobRes] = await Promise.all([
      aliceServer.request('POST', '/api/bookings', { body: payloadAlice }),
      bobServer.request('POST', '/api/bookings', { body: payloadBob }),
    ]);

    const statuses = [aliceRes.status, bobRes.status].sort();
    assert.deepEqual(statuses, [201, 409]);
    const conflict = [aliceRes, bobRes].find((r) => r.status === 409);
    assert.equal(conflict.body.error.code, 'BOOKING_CONFLICT');

    await withTestClient(async (client) => {
      const r = await client.query(
        `SELECT count(*)::int AS n FROM bookings
          WHERE status = 'confirmed'
            AND room_id = $1
            AND tstzrange(starts_at, ends_at, '[)') &&
                tstzrange($2::timestamptz, $3::timestamptz, '[)')`,
        [
          SEED_IDS.roomActive,
          '2026-07-31T16:00:00+08:00',
          '2026-07-31T17:30:00+08:00',
        ],
      );
      assert.equal(r.rows[0].n, 1);
    });
  } finally {
    await aliceServer.close();
    await bobServer.close();
  }
});
