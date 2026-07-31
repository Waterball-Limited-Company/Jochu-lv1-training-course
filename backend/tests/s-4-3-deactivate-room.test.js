import test from 'node:test';
import assert from 'node:assert/strict';
import {
  resetDatabase, seedBaselineUsersAndRooms, insertConfirmedBooking,
  SEED_IDS, SEED_PASSWORD,
} from './helpers/db.js';
import { startTestServer } from './helpers/http.js';
import { taipeiWeekdayDate } from './helpers/time.js';

test('S-4-3 停用只擋新約並保留既有預約', async () => {
  await resetDatabase();
  await seedBaselineUsersAndRooms();
  const futureDate = taipeiWeekdayDate(1);
  const existingId = await insertConfirmedBooking({
    userId: SEED_IDS.alice,
    startsAt: `${futureDate}T10:00:00+08:00`,
    endsAt: `${futureDate}T11:00:00+08:00`,
  });
  const admin = await startTestServer();
  const employee = await startTestServer();
  try {
    await admin.request('POST', '/api/auth/login', {
      body: { username: 'admin', password: SEED_PASSWORD },
    });
    const room = await admin.request('PATCH', `/api/rooms/${SEED_IDS.roomActive}`, {
      body: { is_active: false },
    });
    assert.equal(room.status, 200);
    assert.equal(room.body.is_active, false);

    await employee.request('POST', '/api/auth/login', {
      body: { username: 'alice', password: SEED_PASSWORD },
    });
    const rejected = await employee.request('POST', '/api/bookings', {
      body: {
        room_id: SEED_IDS.roomActive, purpose: '停用後新約', attendee_count: 2,
        needs_projector: false, needs_video_conference: false,
        starts_at: `${futureDate}T14:00:00+08:00`,
        ends_at: `${futureDate}T15:00:00+08:00`,
      },
    });
    assert.equal(rejected.status, 400);
    assert.equal(rejected.body.error.code, 'BOOKING_RULE_VIOLATION');
    const bookings = await employee.request('GET', `/api/bookings?date=${futureDate}`);
    assert.equal(bookings.status, 200);
    const existing = bookings.body.bookings.find(({ id }) => id === existingId);
    assert.equal(existing?.status, 'confirmed');
  } finally {
    await admin.close();
    await employee.close();
  }
});
