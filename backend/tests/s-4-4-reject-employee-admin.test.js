import test from 'node:test';
import assert from 'node:assert/strict';
import {
  resetDatabase, seedBaselineUsersAndRooms, SEED_IDS, SEED_PASSWORD, withTestClient,
} from './helpers/db.js';
import { startTestServer } from './helpers/http.js';

test('S-4-4 一般員工不得執行管理操作', async () => {
  await resetDatabase();
  await seedBaselineUsersAndRooms();
  const server = await startTestServer();
  try {
    await server.request('POST', '/api/auth/login', {
      body: { username: 'alice', password: SEED_PASSWORD },
    });
    const requests = [
      ['POST', '/api/rooms', {
        name: '未授權', floor: '9F', capacity: 2,
        has_projector: false, has_video_conference: false,
      }],
      ['PATCH', `/api/rooms/${SEED_IDS.roomActive}`, { is_active: false }],
      ['POST', `/api/rooms/${SEED_IDS.roomActive}/maintenance-windows`, {
        starts_at: '2026-07-31T10:00:00+08:00',
        ends_at: '2026-07-31T11:00:00+08:00',
      }],
    ];
    for (const [method, path, body] of requests) {
      const res = await server.request(method, path, { body });
      assert.equal(res.status, 403);
      assert.equal(res.body.error.code, 'FORBIDDEN');
    }
    const state = await withTestClient(async (client) => ({
      rooms: (await client.query('SELECT count(*)::int AS n FROM rooms')).rows[0].n,
      active: (await client.query('SELECT is_active FROM rooms WHERE id = $1', [
        SEED_IDS.roomActive,
      ])).rows[0].is_active,
      maintenance: (await client.query(
        'SELECT count(*)::int AS n FROM maintenance_windows',
      )).rows[0].n,
    }));
    assert.deepEqual(state, { rooms: 2, active: true, maintenance: 0 });
  } finally {
    await server.close();
  }
});
