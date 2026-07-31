import test from 'node:test';
import assert from 'node:assert/strict';
import {
  resetDatabase,
  seedBaselineUsersAndRooms,
  insertConfirmedBooking,
  SEED_IDS,
  SEED_PASSWORD,
} from './helpers/db.js';
import { startTestServer } from './helpers/http.js';

const DATE = '2026-07-31';

test('S-2-2 同批預約支援日曆與列表檢視', async () => {
  await resetDatabase();
  await seedBaselineUsersAndRooms();
  await insertConfirmedBooking({
    roomId: SEED_IDS.roomActive,
    userId: SEED_IDS.alice,
    purpose: '上午會',
    startsAt: `${DATE}T10:00:00+08:00`,
    endsAt: `${DATE}T11:00:00+08:00`,
  });
  await insertConfirmedBooking({
    roomId: SEED_IDS.roomActive,
    userId: SEED_IDS.bob,
    purpose: '下午會',
    startsAt: `${DATE}T14:00:00+08:00`,
    endsAt: `${DATE}T15:00:00+08:00`,
  });

  const server = await startTestServer();
  try {
    const login = await server.request('POST', '/api/auth/login', {
      body: { username: 'alice', password: SEED_PASSWORD },
    });
    assert.equal(login.status, 200);

    const res = await server.request('GET', `/api/bookings?date=${DATE}`);
    assert.equal(res.status, 200);
    assert.equal(res.body.date, DATE);
    assert.equal(res.body.timezone, 'Asia/Taipei');
    assert.equal(res.body.bookings.length, 2);

    const starts = res.body.bookings.map((b) => new Date(b.starts_at).getTime());
    assert.deepEqual(starts, [...starts].sort((a, b) => a - b));

    for (const b of res.body.bookings) {
      assert.ok(b.room?.name);
      assert.ok(b.booked_by?.display_name);
      assert.ok(b.purpose);
      assert.equal(b.status, 'confirmed');
    }
  } finally {
    await server.close();
  }
});
