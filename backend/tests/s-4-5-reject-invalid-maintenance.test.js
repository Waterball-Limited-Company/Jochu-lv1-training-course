import test from 'node:test';
import assert from 'node:assert/strict';
import {
  resetDatabase, seedBaselineUsersAndRooms, SEED_IDS, SEED_PASSWORD, withTestClient,
} from './helpers/db.js';
import { startTestServer } from './helpers/http.js';

test('S-4-5 拒絕無效維護起迄', async () => {
  await resetDatabase();
  await seedBaselineUsersAndRooms();
  const server = await startTestServer();
  try {
    await server.request('POST', '/api/auth/login', {
      body: { username: 'admin', password: SEED_PASSWORD },
    });
    for (const endsAt of ['2026-07-31T10:00:00+08:00', '2026-07-31T09:00:00+08:00']) {
      const res = await server.request(
        'POST', `/api/rooms/${SEED_IDS.roomActive}/maintenance-windows`,
        { body: {
          starts_at: '2026-07-31T10:00:00+08:00',
          ends_at: endsAt,
          note: '無效區間',
        } },
      );
      assert.equal(res.status, 400);
      assert.equal(res.body.error.code, 'VALIDATION_ERROR');
      assert.ok(res.body.error.details.some(
        ({ field, reason }) => field === 'ends_at' && reason === 'must_be_after_starts_at',
      ));
    }
    const count = await withTestClient(async (client) =>
      (await client.query(
        'SELECT count(*)::int AS n FROM maintenance_windows',
      )).rows[0].n);
    assert.equal(count, 0);
  } finally {
    await server.close();
  }
});
