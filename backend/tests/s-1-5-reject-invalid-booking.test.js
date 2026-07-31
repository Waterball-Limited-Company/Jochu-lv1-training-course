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

test('S-1-5 拒絕缺漏或無效預約資料', async () => {
  await resetDatabase();
  await seedBaselineUsersAndRooms();

  const server = await startTestServer();
  try {
    const login = await server.request('POST', '/api/auth/login', {
      body: { username: 'alice', password: SEED_PASSWORD },
    });
    assert.equal(login.status, 200);

    const cases = [
      {
        label: '缺少用途',
        body: {
          room_id: SEED_IDS.roomActive,
          attendee_count: 2,
          needs_projector: false,
          needs_video_conference: false,
          starts_at: '2026-07-31T10:00:00+08:00',
          ends_at: '2026-07-31T11:00:00+08:00',
        },
      },
      {
        label: '起迄顛倒',
        body: {
          room_id: SEED_IDS.roomActive,
          purpose: '無效時段',
          attendee_count: 2,
          needs_projector: false,
          needs_video_conference: false,
          starts_at: '2026-07-31T11:00:00+08:00',
          ends_at: '2026-07-31T10:00:00+08:00',
        },
      },
    ];

    for (const c of cases) {
      const res = await server.request('POST', '/api/bookings', { body: c.body });
      assert.equal(res.status, 400, c.label);
      assert.equal(typeof res.body.error.code, 'string', c.label);
      assert.equal(typeof res.body.error.message, 'string', c.label);
    }

    await withTestClient(async (client) => {
      const r = await client.query('SELECT count(*)::int AS n FROM bookings');
      assert.equal(r.rows[0].n, 0);
    });
  } finally {
    await server.close();
  }
});
