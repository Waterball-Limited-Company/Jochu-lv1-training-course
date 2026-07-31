import test from 'node:test';
import assert from 'node:assert/strict';
import {
  assertCanConnect,
  resetDatabase,
  seedBaselineUsersAndRooms,
  withTestClient,
} from './helpers/db.js';
import { startTestServer } from './helpers/http.js';

test('postgres is reachable and schema + seed apply', async () => {
  await assertCanConnect();
  await resetDatabase();
  await seedBaselineUsersAndRooms();
  await withTestClient(async (client) => {
    const users = await client.query('SELECT count(*)::int AS n FROM users');
    const rooms = await client.query('SELECT count(*)::int AS n FROM rooms');
    assert.equal(users.rows[0].n, 3);
    assert.equal(rooms.rows[0].n, 2);
  });
});

test('app loads and health responds', async () => {
  const server = await startTestServer();
  try {
    const res = await server.request('GET', '/api/health');
    assert.equal(res.status, 200);
    assert.equal(res.body.ok, true);
  } finally {
    await server.close();
  }
});
