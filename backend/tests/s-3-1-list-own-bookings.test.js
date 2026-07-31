import test from 'node:test';
import assert from 'node:assert/strict';
import {
  resetDatabase, seedBaselineUsersAndRooms, insertConfirmedBooking,
  SEED_IDS, SEED_PASSWORD, withTestClient, randomUUID,
} from './helpers/db.js';
import { startTestServer } from './helpers/http.js';
import { taipeiWeekdayDate } from './helpers/time.js';

test('S-3-1 我的預約只列出本人紀錄', async () => {
  await resetDatabase();
  await seedBaselineUsersAndRooms();
  const firstFutureDate = taipeiWeekdayDate(1, 1);
  const secondFutureDate = taipeiWeekdayDate(1, 2);
  const thirdFutureDate = taipeiWeekdayDate(1, 3);
  const older = await insertConfirmedBooking({
    userId: SEED_IDS.alice,
    startsAt: `${firstFutureDate}T10:00:00+08:00`,
    endsAt: `${firstFutureDate}T11:00:00+08:00`,
  });
  const newer = randomUUID();
  await withTestClient((client) => client.query(
    `INSERT INTO bookings (
       id, room_id, user_id, purpose, attendee_count,
       needs_projector, needs_video_conference, starts_at, ends_at, status
     ) VALUES ($1,$2,$3,'已取消會議',2,false,false,$4,$5,'cancelled')`,
    [newer, SEED_IDS.roomActive, SEED_IDS.alice,
      `${secondFutureDate}T10:00:00+08:00`, `${secondFutureDate}T11:00:00+08:00`],
  ));
  const other = await insertConfirmedBooking({
    userId: SEED_IDS.bob,
    startsAt: `${thirdFutureDate}T10:00:00+08:00`,
    endsAt: `${thirdFutureDate}T11:00:00+08:00`,
  });

  const server = await startTestServer();
  try {
    assert.equal((await server.request('POST', '/api/auth/login', {
      body: { username: 'alice', password: SEED_PASSWORD },
    })).status, 200);
    const res = await server.request('GET', '/api/bookings/mine');
    assert.equal(res.status, 200);
    assert.deepEqual(res.body.bookings.map(({ id }) => id), [newer, older]);
    assert.ok(!res.body.bookings.some(({ id }) => id === other));
    assert.equal(res.body.bookings[0].status, 'cancelled');
    assert.equal(res.body.bookings[0].is_cancellable, false);
    assert.equal(res.body.bookings[1].is_cancellable, true);
    assert.ok(res.body.bookings.every(({ room }) => room.name && room.floor));
  } finally {
    await server.close();
  }
});
