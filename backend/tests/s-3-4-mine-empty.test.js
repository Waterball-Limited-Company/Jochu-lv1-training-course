import test from 'node:test';
import assert from 'node:assert/strict';
import {
  resetDatabase, seedBaselineUsersAndRooms, SEED_PASSWORD,
} from './helpers/db.js';
import { startTestServer } from './helpers/http.js';

test('S-3-4 沒有自己的預約時回傳空集合', async () => {
  await resetDatabase();
  await seedBaselineUsersAndRooms();
  const server = await startTestServer();
  try {
    await server.request('POST', '/api/auth/login', {
      body: { username: 'alice', password: SEED_PASSWORD },
    });
    const res = await server.request('GET', '/api/bookings/mine');
    assert.equal(res.status, 200);
    assert.deepEqual(res.body.bookings, []);
  } finally {
    await server.close();
  }
});
