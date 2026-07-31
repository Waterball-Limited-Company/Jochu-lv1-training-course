import type { Booking, MaintenanceWindow, Role, Room, User } from './types'

type MockScenario = 'default' | 'unauthenticated' | 'employee' | 'manager' | 'facility_admin' | 'empty-overview' | 'empty-bookings' | 'empty-mine'

const ids = {
  alice: '11111111-1111-4111-8111-111111111111',
  admin: '55555555-5555-4555-8555-555555555555',
  roomA: '22222222-2222-4222-8222-222222222222',
  bookingA: '33333333-3333-4333-8333-333333333333',
  roomB: '66666666-6666-4666-8666-666666666666',
}

const created = '2026-07-30T01:00:00.000Z'
const users: Record<string, User> = {
  alice: { id: ids.alice, username: 'alice', display_name: 'Alice', role: 'employee', created_at: created },
  manager: { id: '88888888-8888-4888-8888-888888888888', username: 'manager', display_name: '主管', role: 'manager', created_at: created },
  admin: { id: ids.admin, username: 'admin', display_name: '設施管理員', role: 'facility_admin', created_at: created },
}

let scenario: MockScenario = 'default'
let currentUser: User | null = users.alice
let rooms: Room[] = []
let bookings: Booking[] = []
let maintenance: MaintenanceWindow[] = []

export class MockApiError extends Error {
  status: number
  code: string
  details: Array<Record<string, unknown>>

  constructor(
    status: number,
    code: string,
    message: string,
    details: Array<Record<string, unknown>> = [],
  ) {
    super(message)
    this.status = status
    this.code = code
    this.details = details
  }
}

export function resetMockApi(next: MockScenario = 'default'): void {
  scenario = next
  const roleByScenario: Partial<Record<MockScenario, Role>> = {
    employee: 'employee',
    manager: 'manager',
    facility_admin: 'facility_admin',
  }
  const role = roleByScenario[next]
  currentUser = next === 'unauthenticated' ? null : role === 'facility_admin' ? users.admin : role === 'manager' ? users.manager : users.alice
  rooms = [
    { id: ids.roomA, name: '大會議 A', floor: '3F', capacity: 12, has_projector: true, has_video_conference: true, is_active: true, created_at: created, updated_at: created },
    { id: ids.roomB, name: '小會議 B', floor: '4F', capacity: 6, has_projector: false, has_video_conference: true, is_active: false, created_at: created, updated_at: created },
  ]
  bookings = next === 'empty-mine' || next === 'empty-bookings' || next === 'empty-overview' ? [] : [
    {
      id: ids.bookingA,
      room_id: ids.roomA,
      user_id: ids.alice,
      purpose: '產品週會',
      attendee_count: 6,
      needs_projector: true,
      needs_video_conference: false,
      starts_at: '2099-08-03T14:00:00+08:00',
      ends_at: '2099-08-03T15:00:00+08:00',
      status: 'confirmed',
      created_at: created,
      updated_at: created,
    },
  ]
  maintenance = []
}

export function setMockScenario(next: MockScenario): void {
  resetMockApi(next)
}

export function getMockScenario(): MockScenario {
  return scenario
}

export async function mockRequest<T>(path: string, init: RequestInit = {}): Promise<T> {
  await Promise.resolve()
  const method = (init.method ?? 'GET').toUpperCase()
  const url = new URL(path, 'http://mock.local')
  const body = init.body ? JSON.parse(String(init.body)) as Record<string, unknown> : {}

  if (url.pathname === '/api/auth/login' && method === 'POST') {
    const username = String(body.username ?? '')
    if (!username || !body.password) throw error(400, 'VALIDATION_ERROR', '請輸入帳號與密碼')
    const user = users[username]
    if (!user || body.password !== 'training-password') throw error(401, 'INVALID_CREDENTIALS', '帳號或密碼錯誤')
    currentUser = user
    return { authenticated: true, user } as T
  }
  if (url.pathname === '/api/auth/me' && method === 'GET') return { authenticated: true, user: requireUser() } as T
  if (url.pathname === '/api/auth/logout' && method === 'POST') {
    requireUser()
    currentUser = null
    return { authenticated: false } as T
  }

  const user = requireUser()
  if (url.pathname === '/api/rooms' && method === 'GET') return { rooms: structuredClone(rooms) } as T
  if (url.pathname === '/api/rooms' && method === 'POST') {
    requireAdmin(user)
    const name = String(body.name ?? '').trim()
    const floor = String(body.floor ?? '').trim()
    const capacity = Number(body.capacity)
    if (!name || !floor || !Number.isInteger(capacity) || capacity < 1 || typeof body.has_projector !== 'boolean' || typeof body.has_video_conference !== 'boolean') {
      throw error(400, 'VALIDATION_ERROR', '請填寫有效的會議室資料')
    }
    const room: Room = {
      id: crypto.randomUUID(), name, floor, capacity,
      has_projector: Boolean(body.has_projector),
      has_video_conference: Boolean(body.has_video_conference),
      is_active: true, created_at: new Date().toISOString(), updated_at: new Date().toISOString(),
    }
    rooms.push(room)
    return structuredClone(room) as T
  }

  const roomPatch = url.pathname.match(/^\/api\/rooms\/([^/]+)$/)
  if (roomPatch && method === 'PATCH') {
    requireAdmin(user)
    if (body.is_active !== false || Object.keys(body).some((key) => key !== 'is_active')) {
      throw error(400, 'VALIDATION_ERROR', 'is_active 必須為 false')
    }
    const room = findRoom(roomPatch[1])
    room.is_active = false
    room.updated_at = new Date().toISOString()
    return structuredClone(room) as T
  }

  const maintenancePath = url.pathname.match(/^\/api\/rooms\/([^/]+)\/maintenance-windows$/)
  if (maintenancePath) {
    const room = findRoom(maintenancePath[1])
    if (method === 'GET') {
      const from = url.searchParams.get('from')
      const to = url.searchParams.get('to')
      if (!from || !to || !Number.isFinite(new Date(from).getTime()) || !Number.isFinite(new Date(to).getTime()) || new Date(to) <= new Date(from)) {
        throw error(400, 'VALIDATION_ERROR', 'from 與 to 必須為有效且順序正確的時間')
      }
      return {
        room_id: room.id,
        maintenance_windows: maintenance.filter((item) =>
          item.room_id === room.id && new Date(item.starts_at) < new Date(to) && new Date(item.ends_at) > new Date(from),
        ),
      } as T
    }
    if (method !== 'POST') throw error(404, 'NOT_FOUND', '找不到 API')
    requireAdmin(user)
    const startsAt = String(body.starts_at ?? '')
    const endsAt = String(body.ends_at ?? '')
    if (
      !startsAt || !endsAt
      || !Number.isFinite(new Date(startsAt).getTime())
      || !Number.isFinite(new Date(endsAt).getTime())
      || new Date(endsAt) <= new Date(startsAt)
    ) {
      throw error(400, 'VALIDATION_ERROR', '結束時間必須晚於開始時間')
    }
    const window: MaintenanceWindow = {
      id: crypto.randomUUID(), room_id: room.id, starts_at: startsAt, ends_at: endsAt,
      note: String(body.note ?? ''), created_by: user.id, created_at: new Date().toISOString(),
    }
    maintenance.push(window)
    return structuredClone(window) as T
  }

  if (url.pathname === '/api/overview/today' && method === 'GET') {
    const empty = scenario === 'empty-overview'
    return {
      date: '2099-08-03',
      timezone: 'Asia/Taipei',
      rooms: rooms.map((room) => {
        const count = empty || room.id !== ids.roomA ? 0 : bookings.filter((booking) => booking.room_id === room.id && booking.status === 'confirmed').length
        return { room_id: room.id, room_name: room.name, is_active: room.is_active, booked_minutes: count * 60, business_minutes: 720, busy_ratio: count / 12, confirmed_booking_count: count }
      }),
    } as T
  }

  if (url.pathname === '/api/bookings' && method === 'GET') {
    const date = url.searchParams.get('date')
    const roomId = url.searchParams.get('roomId')
    if (!date || !/^\d{4}-\d{2}-\d{2}$/.test(date)) throw error(400, 'VALIDATION_ERROR', 'date 必須使用 YYYY-MM-DD')
    if (roomId) findRoom(roomId)
    const result = scenario === 'empty-bookings' ? [] : bookings.filter((booking) =>
      booking.status === 'confirmed' && booking.starts_at.startsWith(date) && (!roomId || booking.room_id === roomId),
    )
    return { date, timezone: 'Asia/Taipei', bookings: result.map(projectBooking) } as T
  }
  if (url.pathname === '/api/bookings' && method === 'POST') {
    const room = findRoom(String(body.room_id ?? ''))
    if (!room.is_active) throw error(400, 'BOOKING_RULE_VIOLATION', '此會議室已停用，無法建立新預約')
    const purpose = String(body.purpose ?? '').trim()
    const attendeeCount = Number(body.attendee_count)
    const startsAt = String(body.starts_at ?? '')
    const endsAt = String(body.ends_at ?? '')
    if (
      !purpose || !Number.isInteger(attendeeCount) || attendeeCount < 1 || !startsAt || !endsAt
      || typeof body.needs_projector !== 'boolean'
      || typeof body.needs_video_conference !== 'boolean'
    ) throw error(400, 'VALIDATION_ERROR', '預約資料不完整')
    const ruleViolation = validateMockBookingWindow(startsAt, endsAt)
    if (ruleViolation) throw error(400, 'BOOKING_RULE_VIOLATION', ruleViolation)
    if (attendeeCount > room.capacity) throw error(400, 'BOOKING_RULE_VIOLATION', '預期人數超過會議室容量')
    if (overlaps(bookings.filter((item) => item.room_id === room.id && item.status === 'confirmed'), startsAt, endsAt)) {
      throw error(409, 'BOOKING_CONFLICT', '該時段已有預約')
    }
    if (overlaps(maintenance.filter((item) => item.room_id === room.id), startsAt, endsAt)) {
      throw error(409, 'MAINTENANCE_CONFLICT', '該時段因維護而不可預約')
    }
    const booking: Booking = {
      id: crypto.randomUUID(), room_id: room.id, user_id: user.id, purpose, attendee_count: attendeeCount,
      needs_projector: Boolean(body.needs_projector), needs_video_conference: Boolean(body.needs_video_conference),
      starts_at: startsAt, ends_at: endsAt, status: 'confirmed', is_cancellable: true,
      created_at: new Date().toISOString(), updated_at: new Date().toISOString(),
    }
    bookings.push(booking)
    return structuredClone(booking) as T
  }
  if (url.pathname === '/api/bookings/mine' && method === 'GET') {
    const mine = scenario === 'empty-mine' ? [] : bookings.filter((booking) => booking.user_id === user.id).map(projectBooking)
    return { bookings: mine } as T
  }
  const cancelPath = url.pathname.match(/^\/api\/bookings\/([^/]+)\/cancel$/)
  if (cancelPath && method === 'POST') {
    const booking = bookings.find((item) => item.id === cancelPath[1])
    if (!booking) throw error(404, 'BOOKING_NOT_FOUND', '找不到預約')
    if (booking.user_id !== user.id) throw error(403, 'FORBIDDEN', '不可取消他人的預約')
    if (booking.status !== 'confirmed') throw error(409, 'BOOKING_NOT_CANCELLABLE', '預約已不可取消')
    booking.status = 'cancelled'
    booking.is_cancellable = false
    booking.updated_at = new Date().toISOString()
    return structuredClone(booking) as T
  }
  throw error(404, 'NOT_FOUND', '找不到 API')
}

function projectBooking(booking: Booking): Booking {
  const room = rooms.find((item) => item.id === booking.room_id)
  const owner = Object.values(users).find((item) => item.id === booking.user_id)
  return {
    ...structuredClone(booking),
    room: room ? { name: room.name, floor: room.floor } : undefined,
    booked_by: owner ? { display_name: owner.display_name } : undefined,
    is_cancellable: booking.status === 'confirmed' && booking.user_id === currentUser?.id,
  }
}

function overlaps(items: Array<{ starts_at: string; ends_at: string }>, start: string, end: string): boolean {
  return items.some((item) => new Date(item.starts_at) < new Date(end) && new Date(item.ends_at) > new Date(start))
}

function validateMockBookingWindow(start: string, end: string): string | null {
  const startDate = new Date(start)
  const endDate = new Date(end)
  if (!Number.isFinite(startDate.getTime()) || !Number.isFinite(endDate.getTime()) || endDate <= startDate) return '預約起迄時間無效'
  if (start.slice(0, 10) !== end.slice(0, 10)) return '預約不可跨日'
  const date = start.slice(0, 10)
  const day = new Date(`${date}T12:00:00+08:00`).getUTCDay()
  if (day === 0 || day === 6 || date === '2099-08-05') return '假日或週末不可預約'
  const startMinutes = Number(start.slice(11, 13)) * 60 + Number(start.slice(14, 16))
  const endMinutes = Number(end.slice(11, 13)) * 60 + Number(end.slice(14, 16))
  const duration = endMinutes - startMinutes
  if (startMinutes < 540 || endMinutes > 1260 || duration < 30 || duration > 240) return '預約須在平日 09:00–21:00，時長 30 分鐘至 4 小時'
  return null
}

function findRoom(id: string): Room {
  const room = rooms.find((item) => item.id === id)
  if (!room) throw error(404, 'ROOM_NOT_FOUND', '找不到會議室')
  return room
}

function requireUser(): User {
  if (!currentUser) throw error(401, 'UNAUTHENTICATED', '請先登入')
  return currentUser
}

function requireAdmin(user: User): void {
  if (user.role !== 'facility_admin') throw error(403, 'FORBIDDEN', '僅設施管理員可執行此操作')
}

function error(status: number, code: string, message: string): MockApiError {
  return new MockApiError(status, code, message)
}

resetMockApi()
