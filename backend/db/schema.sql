CREATE EXTENSION IF NOT EXISTS btree_gist;

-- ========== users ==========
CREATE TABLE users (
  id UUID PRIMARY KEY,
  username TEXT NOT NULL,
  password_hash TEXT NOT NULL,
  display_name TEXT NOT NULL,
  role TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT users_username_nonblank CHECK (btrim(username) <> ''),
  CONSTRAINT users_display_name_nonblank CHECK (btrim(display_name) <> ''),
  CONSTRAINT users_role_allowed CHECK (role IN ('employee', 'manager', 'facility_admin')),
  CONSTRAINT users_username_unique UNIQUE (username)
);

-- ========== rooms ==========
CREATE TABLE rooms (
  id UUID PRIMARY KEY,
  name TEXT NOT NULL,
  floor TEXT NOT NULL,
  capacity INTEGER NOT NULL,
  has_projector BOOLEAN NOT NULL DEFAULT FALSE,
  has_video_conference BOOLEAN NOT NULL DEFAULT FALSE,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT rooms_name_nonblank CHECK (btrim(name) <> ''),
  CONSTRAINT rooms_floor_nonblank CHECK (btrim(floor) <> ''),
  CONSTRAINT rooms_capacity_positive CHECK (capacity >= 1)
);

-- ========== holidays ==========
CREATE TABLE holidays (
  holiday_date DATE PRIMARY KEY,
  name TEXT NOT NULL,
  CONSTRAINT holidays_name_nonblank CHECK (btrim(name) <> '')
);

-- ========== bookings ==========
CREATE TABLE bookings (
  id UUID PRIMARY KEY,
  room_id UUID NOT NULL,
  user_id UUID NOT NULL,
  purpose TEXT NOT NULL,
  attendee_count INTEGER NOT NULL,
  needs_projector BOOLEAN NOT NULL DEFAULT FALSE,
  needs_video_conference BOOLEAN NOT NULL DEFAULT FALSE,
  starts_at TIMESTAMPTZ NOT NULL,
  ends_at TIMESTAMPTZ NOT NULL,
  status TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT bookings_purpose_nonblank CHECK (btrim(purpose) <> ''),
  CONSTRAINT bookings_attendee_positive CHECK (attendee_count >= 1),
  CONSTRAINT bookings_time_order CHECK (ends_at > starts_at),
  CONSTRAINT bookings_status_allowed CHECK (status IN ('confirmed', 'cancelled')),
  CONSTRAINT bookings_room_fk FOREIGN KEY (room_id) REFERENCES rooms (id),
  CONSTRAINT bookings_user_fk FOREIGN KEY (user_id) REFERENCES users (id),
  CONSTRAINT bookings_confirmed_no_overlap EXCLUDE USING gist (
    room_id WITH =,
    tstzrange(starts_at, ends_at, '[)') WITH &&
  ) WHERE (status = 'confirmed')
);

CREATE INDEX bookings_room_time_idx ON bookings (room_id, starts_at, ends_at);
CREATE INDEX bookings_user_idx ON bookings (user_id);
CREATE INDEX bookings_status_idx ON bookings (status);

-- ========== maintenance_windows ==========
CREATE TABLE maintenance_windows (
  id UUID PRIMARY KEY,
  room_id UUID NOT NULL,
  starts_at TIMESTAMPTZ NOT NULL,
  ends_at TIMESTAMPTZ NOT NULL,
  note TEXT,
  created_by UUID NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT maintenance_time_order CHECK (ends_at > starts_at),
  CONSTRAINT maintenance_room_fk FOREIGN KEY (room_id) REFERENCES rooms (id),
  CONSTRAINT maintenance_created_by_fk FOREIGN KEY (created_by) REFERENCES users (id)
);

CREATE INDEX maintenance_room_time_idx ON maintenance_windows (room_id, starts_at, ends_at);
