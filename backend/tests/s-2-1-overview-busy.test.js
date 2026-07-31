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
import { getTaipeiParts } from '../src/lib/time.js';

function taipeiToday() {
  return getTaipeiParts(new Date()).date;
}

async function login(server) {
  const res = await server.request('POST', '/api/auth/login', {
    body: { username: 'alice', password: SEED_PASSWORD },
  });
  assert.equal(res.status, 200);
}

test('S-2-1 今日概況可區分忙碌與空閒', async () => {
  await resetDatabase();
  await seedBaselineUsersAndRooms();
  const today = taipeiToday();
  await insertConfirmedBooking({
    roomId: SEED_IDS.roomActive,
    startsAt: `${today}T10:00:00+08:00`,
    endsAt: `${today}T12:00:00+08:00`,
  });

  const server = await startTestServer();
  try {
    await login(server);
    const res = await server.request('GET', '/api/overview/today');
    assert.equal(res.status, 200);
    assert.equal(res.body.date, today);
    assert.equal(res.body.timezone, 'Asia/Taipei');
    assert.ok(Array.isArray(res.body.rooms));

    const busy = res.body.rooms.find((r) => r.room_id === SEED_IDS.roomActive);
    const idle = res.body.rooms.find((r) => r.room_id === SEED_IDS.roomInactive);
    assert.ok(busy && idle);
    assert.ok(busy.confirmed_booking_count > 0);
    assert.ok(busy.booked_minutes > 0);
    assert.ok(busy.busy_ratio > 0);
    assert.equal(idle.confirmed_booking_count, 0);
    assert.equal(idle.booked_minutes, 0);
    assert.equal(idle.busy_ratio, 0);
  } finally {
    await server.close();
  }
});
