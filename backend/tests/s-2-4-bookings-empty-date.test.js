import test from 'node:test';
import assert from 'node:assert/strict';
import {
  resetDatabase,
  seedBaselineUsersAndRooms,
  SEED_PASSWORD,
} from './helpers/db.js';
import { startTestServer } from './helpers/http.js';

const EMPTY_DATE = '2026-08-04'; // Tuesday with no seed bookings

test('S-2-4 所選日期無預約時回傳空集合', async () => {
  await resetDatabase();
  await seedBaselineUsersAndRooms();

  const server = await startTestServer();
  try {
    const login = await server.request('POST', '/api/auth/login', {
      body: { username: 'alice', password: SEED_PASSWORD },
    });
    assert.equal(login.status, 200);

    const res = await server.request('GET', `/api/bookings?date=${EMPTY_DATE}`);
    assert.equal(res.status, 200);
    assert.equal(res.body.date, EMPTY_DATE);
    assert.equal(res.body.timezone, 'Asia/Taipei');
    assert.deepEqual(res.body.bookings, []);
  } finally {
    await server.close();
  }
});
