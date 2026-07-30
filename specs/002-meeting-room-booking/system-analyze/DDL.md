# DDL：內部共享會議室預約系統

**功能分支**: `002-meeting-room-booking`
**建立日期**: 2026-07-30
**狀態**: 草稿
**對齊**: `system-analyze/data-plan.md`

## DDL

> 單一腳本、多表並以註解區隔。建表順序：`users` → `rooms` → `holidays` → `bookings` → `maintenance_windows`。

```sql
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
```

## 假設

- 引擎為 PostgreSQL 14+（需支援 `btree_gist` 與 partial exclusion）
- 外鍵不設 `ON DELETE CASCADE`：停用／保留歷史預約對齊 GR-003 與關聯設計脈絡；刪使用者屬營運例外，第一版以種子帳號為主
- Session 表由 `connect-pg-simple` 於執行期建立，不納入本腳本
- 營業窗、假日、週末、時長、容量、停用、維護重疊等業務規則由應用層在交易內檢查；本腳本僅落可資料庫化的結構約束
- UUID 由應用層產生後寫入，不依賴 DB `gen_random_uuid()` 擴充（可選加亦可）
