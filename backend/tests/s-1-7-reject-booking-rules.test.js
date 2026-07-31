import test from 'node:test';
import assert from 'node:assert/strict';
import {
  resetDatabase,
  seedBaselineUsersAndRooms,
  insertHoliday,
  SEED_IDS,
  SEED_PASSWORD,
  withTestClient,
} from './helpers/db.js';
import { startTestServer } from './helpers/http.js';

test('S-1-7 拒絕超出可預約日與時段規則', async () => {
  await resetDatabase();
  await seedBaselineUsersAndRooms();
  await insertHoliday('2026-08-03', '種子假日');

  const server = await startTestServer();
  try {
    const login = await server.request('POST', '/api/auth/login', {
      body: { username: 'alice', password: SEED_PASSWORD },
    });
    assert.equal(login.status, 200);

    const violations = [
      {
        label: '跨日',
        body: {
          room_id: SEED_IDS.roomActive,
          purpose: '跨日',
          attendee_count: 2,
          needs_projector: false,
          needs_video_conference: false,
          starts_at: '2026-07-31T20:00:00+08:00',
          ends_at: '2026-08-01T10:00:00+08:00',
        },
      },
      {
        label: '假日',
        body: {
          room_id: SEED_IDS.roomActive,
          purpose: '假日',
          attendee_count: 2,
          needs_projector: false,
          needs_video_conference: false,
          starts_at: '2026-08-03T10:00:00+08:00',
          ends_at: '2026-08-03T11:00:00+08:00',
        },
      },
      {
        label: '過短',
        body: {
          room_id: SEED_IDS.roomActive,
          purpose: '過短',
          attendee_count: 2,
          needs_projector: false,
          needs_video_conference: false,
          starts_at: '2026-07-31T10:00:00+08:00',
          ends_at: '2026-07-31T10:20:00+08:00',
        },
      },
      {
        label: '過長',
        body: {
          room_id: SEED_IDS.roomActive,
          purpose: '過長',
          attendee_count: 2,
          needs_projector: false,
          needs_video_conference: false,
          starts_at: '2026-07-31T09:00:00+08:00',
          ends_at: '2026-07-31T14:00:00+08:00',
        },
      },
      {
        label: '超出營業窗',
        body: {
          room_id: SEED_IDS.roomActive,
          purpose: '過晚',
          attendee_count: 2,
          needs_projector: false,
          needs_video_conference: false,
          starts_at: '2026-07-31T20:30:00+08:00',
          ends_at: '2026-07-31T21:30:00+08:00',
        },
      },
    ];

    for (const v of violations) {
      const res = await server.request('POST', '/api/bookings', { body: v.body });
      assert.equal(res.status, 400, v.label);
      assert.equal(res.body.error.code, 'BOOKING_RULE_VIOLATION', v.label);
      assert.equal(typeof res.body.error.message, 'string', v.label);
    }

    await withTestClient(async (client) => {
      const r = await client.query('SELECT count(*)::int AS n FROM bookings');
      assert.equal(r.rows[0].n, 0);
    });
  } finally {
    await server.close();
  }
});
