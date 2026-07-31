import { describe, expect, it } from 'vitest'
import { ApiError, apiRequest } from '../src/api/client'
import { resetMockApi } from '../src/api/mock'
import type { Booking, MaintenanceWindow, Room } from '../src/api/types'
import { taipeiTimeMinutes, validateBookingWindow } from '../src/lib/datetime-taipei'
import { createRouter } from '../src/router'

const roomA = '22222222-2222-4222-8222-222222222222'
const roomB = '66666666-6666-4666-8666-666666666666'
const bookingA = '33333333-3333-4333-8333-333333333333'

async function visit(url: string): Promise<ReturnType<typeof createRouter>> {
  history.replaceState({}, '', url)
  const router = createRouter(document.querySelector<HTMLElement>('#app')!)
  await router.render()
  return router
}

async function settle(): Promise<void> {
  for (let index = 0; index < 6; index += 1) await new Promise((resolve) => setTimeout(resolve, 0))
}

function setValue(name: string, value: string): void {
  const field = document.querySelector<HTMLInputElement | HTMLSelectElement>(`[name="${name}"]`)!
  field.value = value
  field.dispatchEvent(new Event('change', { bubbles: true }))
}

function submit(selector: string): void {
  document.querySelector<HTMLFormElement>(selector)!.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }))
}

async function loginAs(username: 'alice' | 'manager' | 'admin'): Promise<void> {
  await apiRequest('/api/auth/login', { method: 'POST', body: JSON.stringify({ username, password: 'training-password' }) })
}

async function createBooking(overrides: Record<string, unknown> = {}): Promise<Booking> {
  return apiRequest<Booking>('/api/bookings', {
    method: 'POST',
    body: JSON.stringify({
      room_id: roomA,
      purpose: '設計討論',
      attendee_count: 4,
      needs_projector: false,
      needs_video_conference: false,
      starts_at: '2099-08-04T10:00:00+08:00',
      ends_at: '2099-08-04T11:00:00+08:00',
      ...overrides,
    }),
  })
}

describe('§2 環境與路由', () => {
  it('六個 History 頁面皆可獨立載入並由 URL 還原狀態', async () => {
    resetMockApi('unauthenticated')
    await visit('/login')
    expect(document.querySelector('h1')?.textContent).toBe('登入')
    resetMockApi('facility_admin')
    const routes = [
      ['/home', '今日會議室概況'],
      ['/bookings?date=2099-08-03&roomId=' + roomA + '&view=list', '預約瀏覽'],
      ['/bookings/new?roomId=' + roomA, '建立預約'],
      ['/my-bookings', '我的預約'],
      ['/admin/rooms', '會議室管理'],
    ]
    for (const [url, title] of routes) {
      await visit(url)
      expect(document.querySelector('h1')?.textContent).toBe(title)
    }
    expect((document.querySelector('[name="date"]') as HTMLInputElement | null)?.value).toBeTruthy()
  })

  it('瀏覽器返回與 popstate 會還原前一頁 URL 與內容', async () => {
    const router = await visit(`/bookings?date=2099-08-03&roomId=${roomA}&view=list`)
    router.navigate('/home')
    await settle()
    expect(location.pathname).toBe('/home')
    history.back()
    await settle()
    expect(location.pathname).toBe('/bookings')
    expect((document.querySelector('[name="roomId"]') as HTMLSelectElement).value).toBe(roomA)
    expect(document.querySelector('[data-view="list"]')?.getAttribute('aria-pressed')).toBe('true')
  })
})

describe('US-1 登入、瀏覽與建立預約', () => {
  it('S-1-1 登入後建立合法預約並在我的預約顯示 confirmed', async () => {
    resetMockApi('unauthenticated')
    await visit('/login')
    setValue('username', 'alice')
    setValue('password', 'training-password')
    submit('#login-form')
    await settle()
    expect(location.pathname).toBe('/home')
    await visit(`/bookings/new?roomId=${roomA}`)
    setValue('date', '2099-08-04')
    setValue('start', '10:00')
    setValue('end', '11:00')
    setValue('purpose', '新產品規劃')
    setValue('attendee_count', '5')
    submit('#booking-form')
    await settle()
    expect(location.pathname).toBe('/my-bookings')
    expect(document.body.textContent).toContain('新產品規劃')
    expect(document.body.textContent).toContain('已確認')
  })

  it('S-1-2 重疊時段顯示衝突並保留表單', async () => {
    await visit(`/bookings/new?roomId=${roomA}`)
    setValue('date', '2099-08-03')
    setValue('start', '14:30')
    setValue('end', '15:30')
    setValue('purpose', '重疊測試')
    submit('#booking-form')
    await settle()
    expect(document.querySelector('[data-error]')?.textContent).toContain('已有預約')
    expect((document.querySelector('[name="purpose"]') as HTMLInputElement).value).toBe('重疊測試')
    expect(location.pathname).toBe('/bookings/new')
  })

  it('S-1-3 未登入進入建立預約會導回 Login', async () => {
    resetMockApi('unauthenticated')
    await visit(`/bookings/new?roomId=${roomA}`)
    await settle()
    expect(location.pathname).toBe('/login')
    expect(document.querySelector('#booking-form')).toBeNull()
  })

  it('S-1-4 首頁辨識停用會議室且不提供預約操作', async () => {
    await visit('/home')
    const card = document.querySelector<HTMLElement>(`[data-room-id="${roomB}"]`)!
    expect(card.textContent).toContain('已停用')
    expect(card.querySelector('a[href^="/bookings/new"]')).toBeNull()
  })

  it('S-1-5 缺漏及無效資料顯示可修正原因', async () => {
    await visit(`/bookings/new?roomId=${roomA}`)
    submit('#booking-form')
    await settle()
    expect(document.querySelector('[data-error]')?.textContent).toContain('用途')
    setValue('purpose', '錯誤時段')
    setValue('start', '12:00')
    setValue('end', '11:00')
    submit('#booking-form')
    await settle()
    expect(document.querySelector('[data-error]')?.textContent).toContain('晚於開始')
  })

  it('S-1-7 跨日、假日、過短、過長及營業窗外皆被拒絕', async () => {
    await visit(`/bookings/new?roomId=${roomA}`)
    setValue('purpose', '時段規則測試')
    setValue('date', '2099-08-01')
    submit('#booking-form')
    expect(document.querySelector('[data-error]')?.textContent).toContain('平日')
    setValue('date', '2099-08-04')
    setValue('start', '10:00')
    setValue('end', '10:15')
    submit('#booking-form')
    expect(document.querySelector('[data-error]')?.textContent).toContain('30 分鐘')
    setValue('end', '15:00')
    submit('#booking-form')
    expect(document.querySelector('[data-error]')?.textContent).toContain('4 小時')
    setValue('start', '08:00')
    setValue('end', '10:00')
    submit('#booking-form')
    expect(document.querySelector('[data-error]')?.textContent).toContain('09:00')
    setValue('date', '2099-08-05')
    setValue('start', '10:00')
    setValue('end', '11:00')
    submit('#booking-form')
    await settle()
    expect(document.querySelector('[data-error]')?.textContent).toContain('假日')
    expect((document.querySelector('[name="purpose"]') as HTMLInputElement).value).toBe('時段規則測試')
    expect(document.querySelectorAll('[name="date"]')).toHaveLength(1)
    expect(validateBookingWindow('2099-08-01', '10:00', '11:00')).toContain('平日')
    expect(validateBookingWindow('2099-08-04', '10:00', '10:15')).toContain('30 分鐘')
    expect(validateBookingWindow('2099-08-04', '10:00', '15:00')).toContain('4 小時')
    expect(validateBookingWindow('2099-08-04', '08:00', '10:00')).toContain('09:00')
    await expect(createBooking({ starts_at: '2099-08-04T23:00:00+08:00', ends_at: '2099-08-05T01:00:00+08:00' })).rejects.toMatchObject({ code: 'BOOKING_RULE_VIOLATION' })
    await expect(createBooking({ starts_at: '2099-08-05T10:00:00+08:00', ends_at: '2099-08-05T11:00:00+08:00' })).rejects.toMatchObject({ code: 'BOOKING_RULE_VIOLATION' })
  })
})

describe('US-2 今日概況、日曆與列表', () => {
  it('S-2-1 今日概況區分忙碌與空閒', async () => {
    await visit('/home')
    expect(document.querySelector(`[data-room-id="${roomA}"]`)?.textContent).toContain('忙碌')
    expect(document.querySelector(`[data-room-id="${roomB}"]`)?.textContent).toContain('今日皆空閒')
  })

  it('S-2-2 同一批預約可切換日曆與列表且 URL 還原', async () => {
    await visit(`/bookings?date=2099-08-03&roomId=${roomA}&view=calendar`)
    expect(document.querySelector('.calendar')?.textContent).toContain('產品週會')
    const event = document.querySelector<HTMLElement>('.calendar-event')!
    expect(event.dataset.startMinute).toBe('840')
    expect(event.style.left).toBe('41.66666666666667%')
    expect(document.querySelector('.calendar-room')?.textContent).toContain('大會議 A')
    const scaleLabels = document.querySelectorAll<HTMLElement>('.calendar-scale span')
    expect(scaleLabels).toHaveLength(13)
    expect(scaleLabels[12]?.style.left).toBe('100%')
    ;(document.querySelector('[data-view="list"]') as HTMLButtonElement).click()
    await settle()
    expect(location.search).toContain('view=list')
    expect(document.querySelector('table')?.textContent).toContain('產品週會')
    expect((document.querySelector('[name="roomId"]') as HTMLSelectElement).value).toBe(roomA)
  })

  it('S-2-3 今日無預約仍顯示所有會議室皆空閒', async () => {
    resetMockApi('empty-overview')
    await visit('/home')
    expect(document.querySelectorAll('[data-room-id]')).toHaveLength(2)
    expect(document.querySelectorAll('.busy strong')[0]?.textContent).toContain('皆空閒')
  })

  it('S-2-4 無預約日期在兩種檢視皆顯示空狀態', async () => {
    resetMockApi('empty-bookings')
    await visit('/bookings?date=2099-08-04&view=calendar')
    expect(document.body.textContent).toContain('沒有預約（日曆檢視）')
    await visit('/bookings?date=2099-08-04&view=list')
    expect(document.body.textContent).toContain('沒有預約（列表檢視）')
  })
})

describe('US-3 查看並取消自己的預約', () => {
  it('S-3-1 我的預約列出本人完整紀錄', async () => {
    await visit('/my-bookings')
    expect(document.body.textContent).toContain('大會議 A')
    expect(document.body.textContent).toContain('產品週會')
    expect(document.body.textContent).toContain('需要投影機')
    expect(document.body.textContent).toContain('已確認')
  })

  it('S-3-2 取消後就地更新並釋放時段', async () => {
    await visit('/my-bookings')
    ;(document.querySelector('[data-cancel]') as HTMLButtonElement).click()
    await settle()
    expect(document.querySelector(`[data-booking-id="${bookingA}"]`)?.textContent).toContain('已取消')
    const replacement = await createBooking({ starts_at: '2099-08-03T14:00:00+08:00', ends_at: '2099-08-03T15:00:00+08:00' })
    expect(replacement.status).toBe('confirmed')
  })

  it('S-3-3 我的預約不顯示其他使用者預約', async () => {
    await loginAs('admin')
    await createBooking({ purpose: '管理員私有預約' })
    await loginAs('alice')
    await visit('/my-bookings')
    expect(document.body.textContent).not.toContain('管理員私有預約')
    expect(document.querySelectorAll('[data-booking-id]')).toHaveLength(1)
  })

  it('S-3-4 無本人預約時顯示空狀態與建立入口', async () => {
    resetMockApi('empty-mine')
    await visit('/my-bookings')
    expect(document.body.textContent).toContain('沒有任何預約')
    expect(document.querySelector('a[href="/bookings/new"]')).not.toBeNull()
  })

  it('S-3-5 已取消預約不可再次取消', async () => {
    await apiRequest(`/api/bookings/${bookingA}/cancel`, { method: 'POST' })
    await expect(apiRequest(`/api/bookings/${bookingA}/cancel`, { method: 'POST' })).rejects.toMatchObject({ code: 'BOOKING_NOT_CANCELLABLE' })
    await visit('/my-bookings')
    expect(document.body.textContent).toContain('此預約已不可取消')
    expect(document.querySelector('[data-cancel]')).toBeNull()
  })
})

describe('US-4 設施管理', () => {
  it('S-4-1 管理員新增會議室後員工首頁可見可約', async () => {
    resetMockApi('facility_admin')
    await visit('/admin/rooms')
    setValue('name', '創意室 C')
    setValue('floor', '5F')
    setValue('capacity', '8')
    submit('#room-form')
    await settle()
    expect(document.body.textContent).toContain('創意室 C')
    await loginAs('alice')
    await visit('/home')
    const card = Array.from(document.querySelectorAll('[data-room-id]')).find((item) => item.textContent?.includes('創意室 C'))
    expect(card?.querySelector('a[href^="/bookings/new"]')).not.toBeNull()
  })

  it('S-4-2 維護時段內拒絕新預約並保留輸入', async () => {
    resetMockApi('facility_admin')
    const window = await apiRequest<MaintenanceWindow>(`/api/rooms/${roomA}/maintenance-windows`, {
      method: 'POST',
      body: JSON.stringify({ starts_at: '2099-08-04T10:00:00+08:00', ends_at: '2099-08-04T12:00:00+08:00', note: '空調維修' }),
    })
    expect(window.note).toBe('空調維修')
    await loginAs('alice')
    await visit(`/bookings/new?roomId=${roomA}`)
    setValue('date', '2099-08-04')
    setValue('start', '10:30')
    setValue('end', '11:30')
    setValue('purpose', '維護衝突測試')
    submit('#booking-form')
    await settle()
    expect(document.querySelector('[data-error]')?.textContent).toContain('維護')
    expect((document.querySelector('[name="purpose"]') as HTMLInputElement).value).toBe('維護衝突測試')
  })

  it('S-4-3 停用只擋新約且既有預約維持 confirmed', async () => {
    resetMockApi('facility_admin')
    await apiRequest<Room>(`/api/rooms/${roomA}`, { method: 'PATCH', body: JSON.stringify({ is_active: false }) })
    await loginAs('alice')
    await visit(`/bookings/new?roomId=${roomA}`)
    expect(document.body.textContent).toContain('已停用，不可新約')
    expect((document.querySelector('#booking-form button[type="submit"]') as HTMLButtonElement).disabled).toBe(true)
    await visit('/my-bookings')
    expect(document.body.textContent).toContain('已確認')
  })

  it('S-4-4 一般員工看不到管理入口且直接進入顯示無權', async () => {
    resetMockApi('employee')
    await visit('/home')
    expect(document.querySelector('a[href="/admin/rooms"]')).toBeNull()
    await visit('/admin/rooms')
    expect(document.body.textContent).toContain('只有設施管理員')
    expect(document.querySelector('#room-form')).toBeNull()
  })

  it('S-4-5 無效維護起迄拒絕儲存並保留表單', async () => {
    resetMockApi('facility_admin')
    await visit('/admin/rooms')
    const form = document.querySelector<HTMLFormElement>('#maintenance-form')!
    ;(form.elements.namedItem('start') as HTMLInputElement).value = '12:00'
    ;(form.elements.namedItem('end') as HTMLInputElement).value = '11:00'
    submit('#maintenance-form')
    await settle()
    expect(document.querySelector('[data-admin-error]')?.textContent).toContain('結束時間必須晚於開始時間')
    expect((form.elements.namedItem('start') as HTMLInputElement).value).toBe('12:00')
  })
})

describe('API client 錯誤契約', () => {
  it('一致錯誤包含 status、code 與 message', async () => {
    resetMockApi('unauthenticated')
    const error = await apiRequest('/api/rooms').catch((caught: unknown) => caught)
    expect(error).toBeInstanceOf(ApiError)
    expect(error).toMatchObject({ status: 401, code: 'UNAUTHENTICATED', message: '請先登入' })
  })

  it('Mock 對必填 query、boolean 與 PATCH body 採真 API 契約', async () => {
    await expect(apiRequest('/api/bookings')).rejects.toMatchObject({ status: 400, code: 'VALIDATION_ERROR' })
    await expect(apiRequest(`/api/rooms/${roomA}/maintenance-windows`)).rejects.toMatchObject({ status: 400, code: 'VALIDATION_ERROR' })
    await loginAs('admin')
    await expect(apiRequest('/api/rooms', { method: 'POST', body: JSON.stringify({ name: 'X', floor: '1F', capacity: 1 }) })).rejects.toMatchObject({ status: 400 })
    await expect(apiRequest('/api/rooms', { method: 'POST', body: JSON.stringify({ name: 'X', floor: '1F', capacity: 1.5, has_projector: true, has_video_conference: false }) })).rejects.toMatchObject({ status: 400 })
    await expect(apiRequest(`/api/rooms/${roomA}`, { method: 'PATCH', body: JSON.stringify({ is_active: true }) })).rejects.toMatchObject({ status: 400 })
    await expect(createBooking({ needs_projector: undefined })).rejects.toMatchObject({ status: 400 })
    await expect(createBooking({ attendee_count: 1.5 })).rejects.toMatchObject({ status: 400 })
    await expect(apiRequest(`/api/rooms/${roomA}/maintenance-windows?from=2099-08-01T00:00:00Z&to=2099-08-02T00:00:00Z`, { method: 'DELETE' })).rejects.toMatchObject({ status: 404 })
    await expect(apiRequest(`/api/rooms/${roomA}/maintenance-windows`, { method: 'POST', body: JSON.stringify({ starts_at: 'invalid', ends_at: 'also-invalid' }) })).rejects.toMatchObject({ status: 400 })
  })

  it('UTC Z 時間會依 Asia/Taipei 定位', () => {
    expect(taipeiTimeMinutes('2099-08-03T06:00:00.000Z')).toBe(14 * 60)
  })
})
