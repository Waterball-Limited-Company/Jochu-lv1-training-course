import test from 'node:test';
import assert from 'node:assert/strict';
import {
  resetDatabase, seedBaselineUsersAndRooms, insertConfirmedBooking,
  SEED_IDS, SEED_PASSWORD,
} from './helpers/db.js';
import { startTestServer } from './helpers/http.js';
import { taipeiWeekdayDate } from './helpers/time.js';

test('S-3-2 取消後釋放時段供他人預約', async () => {
  await resetDatabase();
  await seedBaselineUsersAndRooms();
  const futureDate = taipeiWeekdayDate(1);
  const bookingBody = {
    room_id: SEED_IDS.roomActive,
    purpose: '接手時段',
    attendee_count: 2,
    needs_projector: false,
    needs_video_conference: false,
    starts_at: `${futureDate}T14:00:00+08:00`,
    ends_at: `${futureDate}T15:00:00+08:00`,
  };
  const bookingId = await insertConfirmedBooking({
    userId: SEED_IDS.alice,
    startsAt: bookingBody.starts_at,
    endsAt: bookingBody.ends_at,
  });
  const alice = await startTestServer();
  const bob = await startTestServer();
  try {
    assert.equal((await alice.request('POST', '/api/auth/login', {
      body: { username: 'alice', password: SEED_PASSWORD },
    })).status, 200);
    assert.equal((await bob.request('POST', '/api/auth/login', {
      body: { username: 'bob', password: SEED_PASSWORD },
    })).status, 200);

    const cancelled = await alice.request('POST', `/api/bookings/${bookingId}/cancel`);
    assert.equal(cancelled.status, 200);
    assert.equal(cancelled.body.status, 'cancelled');

    const replacement = await bob.request('POST', '/api/bookings', { body: bookingBody });
    assert.equal(replacement.status, 201);
    assert.equal(replacement.body.user_id, SEED_IDS.bob);
    assert.equal(replacement.body.status, 'confirmed');
  } finally {
    await alice.close();
    await bob.close();
  }
});
