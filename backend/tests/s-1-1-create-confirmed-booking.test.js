import test from 'node:test';
import assert from 'node:assert/strict';
import {
  assertCanConnect,
  resetDatabase,
  seedBaselineUsersAndRooms,
  SEED_IDS,
  SEED_PASSWORD,
  withTestClient,
} from './helpers/db.js';
import { startTestServer } from './helpers/http.js';

test('S-1-1 登入後建立合法預約並確認', async () => {
  await resetDatabase();
  await seedBaselineUsersAndRooms();

  const server = await startTestServer();
  try {
    const login = await server.request('POST', '/api/auth/login', {
      body: {
        username: 'alice',
        password: SEED_PASSWORD,
      },
    });

    assert.equal(login.status, 200);
    assert.equal(login.body.authenticated, true);
    assert.equal(login.body.user.id, SEED_IDS.alice);
    assert.equal(login.body.user.username, 'alice');
    assert.equal(login.body.user.role, 'employee');
    assert.ok(server.jar.size > 0, '登入後應建立可供後續請求使用的 session cookie');

    const rooms = await server.request('GET', '/api/rooms');

    assert.equal(rooms.status, 200);
    assert.ok(Array.isArray(rooms.body.rooms));
    assert.ok(
      rooms.body.rooms.some(
        (room) =>
          room.id === SEED_IDS.roomActive &&
          room.name === 'Sunrise' &&
          room.floor === '3F' &&
          room.capacity === 8 &&
          room.has_projector === true &&
          room.has_video_conference === true &&
          room.is_active === true,
      ),
      '會議室清單應包含啟用中的目標會議室及其屬性',
    );

    const bookingRequest = {
      room_id: SEED_IDS.roomActive,
      purpose: '產品週會',
      attendee_count: 6,
      needs_projector: true,
      needs_video_conference: false,
      starts_at: '2026-07-31T14:00:00+08:00',
      ends_at: '2026-07-31T15:00:00+08:00',
    };
    const booking = await server.request('POST', '/api/bookings', {
      body: bookingRequest,
    });

    assert.equal(booking.status, 201);
    assert.match(booking.body.id, /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i);
    assert.equal(booking.body.room_id, SEED_IDS.roomActive);
    assert.equal(booking.body.user_id, SEED_IDS.alice);
    assert.equal(booking.body.purpose, bookingRequest.purpose);
    assert.equal(booking.body.attendee_count, bookingRequest.attendee_count);
    assert.equal(booking.body.needs_projector, bookingRequest.needs_projector);
    assert.equal(
      booking.body.needs_video_conference,
      bookingRequest.needs_video_conference,
    );
    assert.equal(
      new Date(booking.body.starts_at).getTime(),
      new Date(bookingRequest.starts_at).getTime(),
    );
    assert.equal(
      new Date(booking.body.ends_at).getTime(),
      new Date(bookingRequest.ends_at).getTime(),
    );
    assert.equal(booking.body.status, 'confirmed');

    await withTestClient(async (client) => {
      const persisted = await client.query(
        `SELECT room_id, user_id, purpose, attendee_count,
                needs_projector, needs_video_conference, starts_at, ends_at, status
           FROM bookings
          WHERE id = $1`,
        [booking.body.id],
      );

      assert.equal(persisted.rowCount, 1);
      assert.equal(persisted.rows[0].room_id, SEED_IDS.roomActive);
      assert.equal(persisted.rows[0].user_id, SEED_IDS.alice);
      assert.equal(persisted.rows[0].status, 'confirmed');
    });
  } finally {
    await server.close();
  }
});
