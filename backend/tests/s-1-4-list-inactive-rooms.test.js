import test from 'node:test';
import assert from 'node:assert/strict';
import {
  resetDatabase,
  seedBaselineUsersAndRooms,
  SEED_IDS,
  SEED_PASSWORD,
} from './helpers/db.js';
import { startTestServer } from './helpers/http.js';

test('S-1-4 清單可辨識停用會議室', async () => {
  await resetDatabase();
  await seedBaselineUsersAndRooms();

  const server = await startTestServer();
  try {
    const login = await server.request('POST', '/api/auth/login', {
      body: { username: 'alice', password: SEED_PASSWORD },
    });
    assert.equal(login.status, 200);

    const rooms = await server.request('GET', '/api/rooms');
    assert.equal(rooms.status, 200);
    assert.ok(Array.isArray(rooms.body.rooms));

    const active = rooms.body.rooms.find((r) => r.id === SEED_IDS.roomActive);
    const inactive = rooms.body.rooms.find((r) => r.id === SEED_IDS.roomInactive);
    assert.ok(active, '應保留啟用會議室');
    assert.ok(inactive, '應保留停用會議室');
    assert.equal(active.is_active, true);
    assert.equal(inactive.is_active, false);
  } finally {
    await server.close();
  }
});
