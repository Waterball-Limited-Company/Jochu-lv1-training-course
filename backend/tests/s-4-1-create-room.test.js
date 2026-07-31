import test from 'node:test';
import assert from 'node:assert/strict';
import {
  resetDatabase, seedBaselineUsersAndRooms, SEED_PASSWORD,
} from './helpers/db.js';
import { startTestServer } from './helpers/http.js';

test('S-4-1 新增會議室後員工可見可約', async () => {
  await resetDatabase();
  await seedBaselineUsersAndRooms();
  const admin = await startTestServer();
  const employee = await startTestServer();
  try {
    await admin.request('POST', '/api/auth/login', {
      body: { username: 'admin', password: SEED_PASSWORD },
    });
    const created = await admin.request('POST', '/api/rooms', {
      body: {
        name: '研討室 C', floor: '6F', capacity: 6,
        has_projector: true, has_video_conference: false,
      },
    });
    assert.equal(created.status, 201);
    assert.equal(created.body.is_active, true);

    await employee.request('POST', '/api/auth/login', {
      body: { username: 'alice', password: SEED_PASSWORD },
    });
    const rooms = await employee.request('GET', '/api/rooms');
    assert.ok(rooms.body.rooms.some(({ id }) => id === created.body.id));
    const booking = await employee.request('POST', '/api/bookings', {
      body: {
        room_id: created.body.id, purpose: '新會議室首約', attendee_count: 4,
        needs_projector: true, needs_video_conference: false,
        starts_at: '2026-07-31T10:00:00+08:00',
        ends_at: '2026-07-31T11:00:00+08:00',
      },
    });
    assert.equal(booking.status, 201);
  } finally {
    await admin.close();
    await employee.close();
  }
});
