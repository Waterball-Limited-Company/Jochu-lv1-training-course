import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import {
  insertConfirmedBooking,
  resetDatabase,
  seedBaselineUsersAndRooms,
  SEED_IDS,
  SEED_PASSWORD,
} from '../../../backend/tests/helpers/db.js'
import { startTestServer } from '../../../backend/tests/helpers/http.js'
import { taipeiWeekdayDate } from '../../../backend/tests/helpers/time.js'
import { setApiBaseUrl } from '../../src/api/client'
import { createRouter } from '../../src/router'

type BrowserResponse = {
  status: number
  body: Record<string, any>
}

type BrowserSession = {
  activate: () => void
  request: (method: string, path: string, body?: Record<string, unknown>) => Promise<BrowserResponse>
}

const nativeFetch = globalThis.fetch
let server: Awaited<ReturnType<typeof startTestServer>>

function createBrowserSession(): BrowserSession {
  let cookie = ''
  const sessionFetch: typeof fetch = async (input, init = {}) => {
    const headers = new Headers(init.headers)
    if (cookie) headers.set('cookie', cookie)
    const response = await nativeFetch(input, { ...init, headers })
    const setCookie = response.headers.get('set-cookie')
    if (setCookie) cookie = setCookie.split(';', 1)[0]
    return response
  }
  return {
    activate() {
      globalThis.fetch = sessionFetch
    },
    async request(method, path, body) {
      const response = await sessionFetch(`${server.baseUrl}${path}`, {
        method,
        headers: body ? { 'content-type': 'application/json' } : undefined,
        body: body ? JSON.stringify(body) : undefined,
      })
      return {
        status: response.status,
        body: await response.json() as Record<string, any>,
      }
    },
  }
}

async function login(session: BrowserSession, username: 'alice' | 'bob' | 'admin'): Promise<void> {
  const response = await session.request('POST', '/api/auth/login', {
    username,
    password: SEED_PASSWORD,
  })
  expect(response.status).toBe(200)
}

async function visit(url: string): Promise<ReturnType<typeof createRouter>> {
  history.replaceState({}, '', url)
  const router = createRouter(document.querySelector<HTMLElement>('#app')!)
  await router.render()
  return router
}

async function waitFor(assertion: () => void): Promise<void> {
  const deadline = Date.now() + 4_000
  let lastError: unknown
  while (Date.now() < deadline) {
    try {
      assertion()
      return
    } catch (error) {
      lastError = error
      await new Promise((resolve) => setTimeout(resolve, 10))
    }
  }
  throw lastError
}

function setValue(name: string, value: string): void {
  const field = document.querySelector<HTMLInputElement | HTMLSelectElement>(`[name="${name}"]`)
  if (!field) throw new Error(`missing form field: ${name}`)
  field.value = value
  field.dispatchEvent(new Event('change', { bubbles: true }))
}

function submit(selector: string): void {
  const form = document.querySelector<HTMLFormElement>(selector)
  if (!form) throw new Error(`missing form: ${selector}`)
  form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }))
}

function bookingPayload(
  date: string,
  purpose: string,
  overrides: Record<string, unknown> = {},
): Record<string, unknown> {
  return {
    room_id: SEED_IDS.roomActive,
    purpose,
    attendee_count: 2,
    needs_projector: false,
    needs_video_conference: false,
    starts_at: `${date}T14:00:00+08:00`,
    ends_at: `${date}T15:00:00+08:00`,
    ...overrides,
  }
}

beforeEach(async () => {
  globalThis.fetch = nativeFetch
  await resetDatabase()
  await seedBaselineUsersAndRooms()
  server = await startTestServer()
  setApiBaseUrl(server.baseUrl)
})

afterEach(async () => {
  globalThis.fetch = nativeFetch
  await server.close()
})

describe('前後端真串接整合 Scenario', () => {
  it('S-1-1 登入後跨頁建立合法預約並由後端重新讀取', async () => {
    const date = taipeiWeekdayDate(1)
    const employee = createBrowserSession()
    employee.activate()

    await visit('/login')
    setValue('username', 'alice')
    setValue('password', SEED_PASSWORD)
    submit('#login-form')
    await waitFor(() => {
      expect(location.pathname).toBe('/home')
      expect(document.querySelector(`[data-room-id="${SEED_IDS.roomActive}"]`)).not.toBeNull()
    })

    const bookingLink = document.querySelector<HTMLAnchorElement>(
      `[data-room-id="${SEED_IDS.roomActive}"] a[href^="/bookings/new"]`,
    )
    bookingLink?.click()
    await waitFor(() => expect(document.querySelector('#booking-form')).not.toBeNull())
    setValue('date', date)
    setValue('start', '10:00')
    setValue('end', '11:00')
    setValue('purpose', '整合跨頁預約')
    setValue('attendee_count', '5')
    submit('#booking-form')

    await waitFor(() => {
      expect(location.pathname).toBe('/my-bookings')
      expect(document.body.textContent).toContain('整合跨頁預約')
      expect(document.body.textContent).toContain('已確認')
    })
    await visit('/home')
    await visit('/my-bookings')
    expect(document.body.textContent).toContain('整合跨頁預約')
    expect(document.body.textContent).toContain('已確認')
  })

  it('S-1-6 兩個 cookie session 的併發重疊預約只確認一筆', async () => {
    const date = taipeiWeekdayDate(1)
    const alice = createBrowserSession()
    const bob = createBrowserSession()
    await Promise.all([login(alice, 'alice'), login(bob, 'bob')])

    const [aliceResult, bobResult] = await Promise.all([
      alice.request('POST', '/api/bookings', bookingPayload(date, 'Alice 併發')),
      bob.request('POST', '/api/bookings', bookingPayload(date, 'Bob 併發', {
        starts_at: `${date}T14:30:00+08:00`,
        ends_at: `${date}T15:30:00+08:00`,
      })),
    ])

    expect([aliceResult.status, bobResult.status].sort()).toEqual([201, 409])
    const conflict = [aliceResult, bobResult].find(({ status }) => status === 409)!
    expect(conflict.body).toMatchObject({
      error: {
        code: 'BOOKING_CONFLICT',
        message: expect.any(String),
      },
    })

    const finalState = await alice.request('GET', `/api/bookings?date=${date}`)
    expect(finalState.status).toBe(200)
    const overlapping = finalState.body.bookings.filter(
      (booking: Record<string, unknown>) => booking.room_id === SEED_IDS.roomActive,
    )
    expect(overlapping).toHaveLength(1)
    expect(overlapping[0].status).toBe('confirmed')
  })

  it('S-3-2 取消後另一位員工可在獨立 session 預約同時段', async () => {
    const date = taipeiWeekdayDate(1)
    const originalId = await insertConfirmedBooking({
      userId: SEED_IDS.alice,
      purpose: 'Alice 原預約',
      startsAt: `${date}T10:00:00+08:00`,
      endsAt: `${date}T11:00:00+08:00`,
    })
    const alice = createBrowserSession()
    const bob = createBrowserSession()
    await Promise.all([login(alice, 'alice'), login(bob, 'bob')])

    const blocked = await bob.request(
      'POST',
      '/api/bookings',
      bookingPayload(date, 'Bob 第一次嘗試', {
        starts_at: `${date}T10:00:00+08:00`,
        ends_at: `${date}T11:00:00+08:00`,
      }),
    )
    expect(blocked.status).toBe(409)
    expect(blocked.body.error.code).toBe('BOOKING_CONFLICT')

    alice.activate()
    await visit('/my-bookings')
    document.querySelector<HTMLButtonElement>(`[data-booking-id="${originalId}"] [data-cancel]`)?.click()
    await waitFor(() => {
      expect(document.querySelector(`[data-booking-id="${originalId}"]`)?.textContent).toContain('已取消')
    })

    const replacement = await bob.request(
      'POST',
      '/api/bookings',
      bookingPayload(date, 'Bob 接手預約', {
        starts_at: `${date}T10:00:00+08:00`,
        ends_at: `${date}T11:00:00+08:00`,
      }),
    )
    expect(replacement.status).toBe(201)
    expect(replacement.body.status).toBe('confirmed')

    alice.activate()
    await visit('/my-bookings')
    expect(document.querySelector(`[data-booking-id="${originalId}"]`)?.textContent).toContain('已取消')
    bob.activate()
    await visit('/my-bookings')
    expect(document.body.textContent).toContain('Bob 接手預約')
    expect(document.body.textContent).toContain('已確認')
  })

  it('S-4-3 管理員停用後阻擋新約並保留既有預約', async () => {
    const date = taipeiWeekdayDate(1)
    const existingId = await insertConfirmedBooking({
      userId: SEED_IDS.alice,
      purpose: '停用前既有預約',
      startsAt: `${date}T10:00:00+08:00`,
      endsAt: `${date}T11:00:00+08:00`,
    })
    const admin = createBrowserSession()
    const employee = createBrowserSession()
    await Promise.all([login(admin, 'admin'), login(employee, 'alice')])

    admin.activate()
    await visit('/admin/rooms')
    document.querySelector<HTMLButtonElement>(`[data-deactivate="${SEED_IDS.roomActive}"]`)?.click()
    await waitFor(() => {
      expect(document.querySelector(`[data-admin-room="${SEED_IDS.roomActive}"]`)?.textContent)
        .toContain('已停用')
    })

    employee.activate()
    await visit('/home')
    const roomCard = document.querySelector(`[data-room-id="${SEED_IDS.roomActive}"]`)
    expect(roomCard?.textContent).toContain('已停用')
    expect(roomCard?.querySelector('a[href^="/bookings/new"]')).toBeNull()
    await visit(`/bookings/new?roomId=${SEED_IDS.roomActive}`)
    expect(document.body.textContent).toContain('已停用，不可新約')
    expect(document.querySelector<HTMLButtonElement>('#booking-form button[type="submit"]')?.disabled)
      .toBe(true)

    const rejected = await employee.request(
      'POST',
      '/api/bookings',
      bookingPayload(date, '停用後新約', {
        starts_at: `${date}T14:00:00+08:00`,
        ends_at: `${date}T15:00:00+08:00`,
      }),
    )
    expect(rejected.status).toBe(400)
    expect(rejected.body).toMatchObject({
      error: {
        code: 'BOOKING_RULE_VIOLATION',
        message: expect.any(String),
      },
    })

    await visit(`/bookings?date=${date}&view=list`)
    expect(document.body.textContent).toContain('停用前既有預約')
    await visit('/my-bookings')
    expect(document.querySelector(`[data-booking-id="${existingId}"]`)?.textContent).toContain('已確認')
    expect(document.body.textContent).not.toContain('停用後新約')
  })
})
