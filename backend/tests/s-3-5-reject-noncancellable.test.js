import test from 'node:test';
import assert from 'node:assert/strict';
import {
  resetDatabase, seedBaselineUsersAndRooms, insertConfirmedBooking,
  SEED_IDS, SEED_PASSWORD, withTestClient, randomUUID,
} from './helpers/db.js';
import { startTestServer } from './helpers/http.js';
import { taipeiWeekdayDate } from './helpers/time.js';

test('S-3-5 已結束或已取消預約不可再次取消', async () => {
  await resetDatabase();
  await seedBaselineUsersAndRooms();
  const pastDate = taipeiWeekdayDate(-1);
  const futureDate = taipeiWeekdayDate(1);
  const endedId = await insertConfirmedBooking({
    userId: SEED_IDS.alice,
    startsAt: `${pastDate}T09:00:00+08:00`,
    endsAt: `${pastDate}T10:00:00+08:00`,
  });
  const cancelledId = randomUUID();
  await withTestClient((client) => client.query(
    `INSERT INTO bookings (
       id, room_id, user_id, purpose, attendee_count,
       needs_projector, needs_video_conference, starts_at, ends_at, status
     ) VALUES ($1,$2,$3,'已取消',2,false,false,$4,$5,'cancelled')`,
    [cancelledId, SEED_IDS.roomActive, SEED_IDS.alice,
      `${futureDate}T12:00:00+08:00`, `${futureDate}T13:00:00+08:00`],
  ));
  const server = await startTestServer();
  try {
    await server.request('POST', '/api/auth/login', {
      body: { username: 'alice', password: SEED_PASSWORD },
    });
    for (const id of [endedId, cancelledId]) {
      const res = await server.request('POST', `/api/bookings/${id}/cancel`);
      assert.equal(res.status, 409);
      assert.equal(res.body.error.code, 'BOOKING_NOT_CANCELLABLE');
    }
    const rows = await withTestClient(async (client) =>
      (await client.query(
        'SELECT id, status FROM bookings WHERE id = ANY($1::uuid[]) ORDER BY id',
        [[endedId, cancelledId]],
      )).rows);
    assert.deepEqual(rows.map(({ status }) => status).sort(), ['cancelled', 'confirmed']);
  } finally {
    await server.close();
  }
});
