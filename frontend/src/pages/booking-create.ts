import { apiRequest, errorMessage } from '../api/client'
import type { Booking, MaintenanceWindow, Room } from '../api/types'
import { escapeHtml, pageShell } from '../components/ui'
import { toTaipeiIso, todayInTaipei, validateBookingWindow } from '../lib/datetime-taipei'
import type { PageContext } from '../router'

export async function renderBookingCreate(context: PageContext): Promise<void> {
  const user = await context.requireUser()
  if (!user) return
  try {
    const response = await apiRequest<{ rooms: Room[] }>('/api/rooms')
    const requestedRoomId = new URLSearchParams(location.search).get('roomId') ?? ''
    const selected = response.rooms.find((room) => room.id === requestedRoomId) ?? response.rooms.find((room) => room.is_active) ?? response.rooms[0]
    context.root.innerHTML = pageShell('建立預約', `
      <section class="card">
        <form id="booking-form" novalidate>
          <div class="form-grid">
            <label>會議室<select name="room_id" required>${response.rooms.map((room) => `<option value="${room.id}" ${room.id === selected?.id ? 'selected' : ''}>${escapeHtml(room.name)}${room.is_active ? '' : '（已停用）'}</option>`).join('')}</select></label>
            <label>日期<input name="date" type="date" value="${todayInTaipei()}" required></label>
            <label>開始時間<input name="start" type="time" value="09:00" required></label>
            <label>結束時間<input name="end" type="time" value="10:00" required></label>
            <label class="wide">用途<input name="purpose" required></label>
            <label>預期人數<input name="attendee_count" type="number" min="1" value="1" required></label>
            <label class="check"><input name="needs_projector" type="checkbox">需要投影機</label>
            <label class="check"><input name="needs_video_conference" type="checkbox">需要視訊設備</label>
          </div>
          <p class="hint">僅限台北平日 09:00–21:00，同日 30 分鐘至 4 小時；後端判定為最終真相。</p>
          <div data-room-state>${roomState(selected)}</div>
          <div data-maintenance class="maintenance-hint"></div>
          <p class="form-error" data-error aria-live="polite"></p>
          <button type="submit" ${selected?.is_active ? '' : 'disabled'}>建立預約</button>
        </form>
      </section>`, user)
    bindBookingForm(context, response.rooms)
  } catch (caught) {
    context.root.innerHTML = pageShell('建立預約', `<div class="state error">${escapeHtml(errorMessage(caught))}<button data-action="retry">重試</button></div>`, user)
  }
}

function bindBookingForm(context: PageContext, rooms: Room[]): void {
  const form = context.root.querySelector<HTMLFormElement>('#booking-form')!
  const updateRoom = async (): Promise<void> => {
    const data = new FormData(form)
    const room = rooms.find((item) => item.id === data.get('room_id'))
    form.querySelector<HTMLElement>('[data-room-state]')!.innerHTML = roomState(room)
    form.querySelector<HTMLButtonElement>('button[type="submit"]')!.disabled = !room?.is_active
    const params = new URLSearchParams({ roomId: String(data.get('room_id') ?? '') })
    history.replaceState({}, '', `/bookings/new?${params}`)
    await loadMaintenance(form)
  }
  ;(form.elements.namedItem('room_id') as HTMLSelectElement | null)?.addEventListener('change', () => void updateRoom())
  ;(form.elements.namedItem('date') as HTMLInputElement | null)?.addEventListener('change', () => void loadMaintenance(form))
  form.addEventListener('submit', async (event) => {
    event.preventDefault()
    const data = new FormData(form)
    const error = form.querySelector<HTMLElement>('[data-error]')!
    error.textContent = ''
    const purpose = String(data.get('purpose') ?? '').trim()
    const attendees = Number(data.get('attendee_count'))
    const windowError = validateBookingWindow(String(data.get('date')), String(data.get('start')), String(data.get('end')))
    if (!purpose) error.textContent = '請填寫用途'
    else if (!Number.isInteger(attendees) || attendees < 1) error.textContent = '預期人數必須為正整數'
    else if (windowError) error.textContent = windowError
    if (error.textContent) return
    const button = form.querySelector<HTMLButtonElement>('button[type="submit"]')!
    button.disabled = true
    button.textContent = '建立中…'
    try {
      const booking = await apiRequest<Booking>('/api/bookings', {
        method: 'POST',
        body: JSON.stringify({
          room_id: data.get('room_id'),
          purpose,
          attendee_count: attendees,
          needs_projector: data.get('needs_projector') === 'on',
          needs_video_conference: data.get('needs_video_conference') === 'on',
          starts_at: toTaipeiIso(String(data.get('date')), String(data.get('start'))),
          ends_at: toTaipeiIso(String(data.get('date')), String(data.get('end'))),
        }),
      })
      sessionStorage.setItem('booking-flash', `預約「${booking.purpose}」已確認`)
      context.navigate('/my-bookings')
    } catch (caught) {
      error.textContent = errorMessage(caught)
      button.disabled = false
      button.textContent = '建立預約'
    }
  })
  void loadMaintenance(form)
}

async function loadMaintenance(form: HTMLFormElement): Promise<void> {
  const data = new FormData(form)
  const roomId = String(data.get('room_id') ?? '')
  const date = String(data.get('date') ?? '')
  const target = form.querySelector<HTMLElement>('[data-maintenance]')!
  if (!roomId || !date) return
  try {
    const response = await apiRequest<{ maintenance_windows: MaintenanceWindow[] }>(
      `/api/rooms/${roomId}/maintenance-windows?from=${encodeURIComponent(toTaipeiIso(date, '00:00'))}&to=${encodeURIComponent(toTaipeiIso(date, '23:59'))}`,
    )
    target.textContent = response.maintenance_windows.length
      ? `維護時段：${response.maintenance_windows.map((item) => `${formatMaintenanceTime(item.starts_at)}–${formatMaintenanceTime(item.ends_at)} ${item.note ?? ''}`.trim()).join('、')}`
      : '當日無已知維護時段'
  } catch {
    target.textContent = '暫時無法取得維護時段，送出時仍會由伺服器確認'
  }
}

function roomState(room?: Room): string {
  if (!room) return '<p class="form-error">目前沒有可選會議室</p>'
  return `<p class="${room.is_active ? 'success-text' : 'form-error'}">${escapeHtml(room.name)} · ${escapeHtml(room.floor)} · 容量 ${room.capacity} 人 · ${room.is_active ? '可預約' : '已停用，不可新約'}</p>`
}

function formatMaintenanceTime(value: string): string {
  return new Intl.DateTimeFormat('zh-TW', {
    timeZone: 'Asia/Taipei',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  }).format(new Date(value))
}
