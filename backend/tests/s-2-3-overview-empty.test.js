import test from 'node:test';
import assert from 'node:assert/strict';
import {
  resetDatabase,
  seedBaselineUsersAndRooms,
  SEED_IDS,
  SEED_PASSWORD,
} from './helpers/db.js';
import { startTestServer } from './helpers/http.js';
import { getTaipeiParts } from '../src/lib/time.js';

test('S-2-3 今日無預約仍回傳可理解概況', async () => {
  await resetDatabase();
  await seedBaselineUsersAndRooms();
  const today = getTaipeiParts(new Date()).date;

  const server = await startTestServer();
  try {
    const login = await server.request('POST', '/api/auth/login', {
      body: { username: 'alice', password: SEED_PASSWORD },
    });
    assert.equal(login.status, 200);

    const res = await server.request('GET', '/api/overview/today');
    assert.equal(res.status, 200);
    assert.equal(res.body.date, today);
    assert.equal(res.body.rooms.length, 2);
    for (const room of res.body.rooms) {
      assert.ok([SEED_IDS.roomActive, SEED_IDS.roomInactive].includes(room.room_id));
      assert.equal(room.confirmed_booking_count, 0);
      assert.equal(room.booked_minutes, 0);
      assert.equal(room.busy_ratio, 0);
    }
  } finally {
    await server.close();
  }
});
