import { apiRequest, errorMessage } from '../api/client'
import type { Booking, Room } from '../api/types'
import { emptyState, escapeHtml, pageShell } from '../components/ui'
import { formatTaipeiDateTime, taipeiTimeMinutes, todayInTaipei } from '../lib/datetime-taipei'
import type { PageContext } from '../router'

export async function renderBookingsBrowse(context: PageContext): Promise<void> {
  const user = await context.requireUser()
  if (!user) return
  const params = new URLSearchParams(location.search)
  const date = params.get('date') ?? todayInTaipei()
  const roomId = params.get('roomId') ?? ''
  const view = params.get('view') === 'list' ? 'list' : 'calendar'
  try {
    const [roomResponse, bookingResponse] = await Promise.all([
      apiRequest<{ rooms: Room[] }>('/api/rooms'),
      apiRequest<{ bookings: Booking[] }>(`/api/bookings?date=${date}${roomId ? `&roomId=${roomId}` : ''}`),
    ])
    const controls = `<form id="browse-controls" class="filters">
      <label>日期<input name="date" type="date" value="${escapeHtml(date)}"></label>
      <label>會議室<select name="roomId"><option value="">全部會議室</option>${roomResponse.rooms.map((room) => `<option value="${room.id}" ${room.id === roomId ? 'selected' : ''}>${escapeHtml(room.name)}</option>`).join('')}</select></label>
      <div class="segmented" aria-label="檢視模式">
        <button type="button" data-view="calendar" aria-pressed="${view === 'calendar'}">日曆</button>
        <button type="button" data-view="list" aria-pressed="${view === 'list'}">列表</button>
      </div>
    </form>`
    context.root.innerHTML = pageShell('預約瀏覽', `${controls}${renderBookings(bookingResponse.bookings, view)}`, user)
    context.root.querySelector<HTMLFormElement>('#browse-controls')?.addEventListener('change', (event) => {
      const form = event.currentTarget as HTMLFormElement
      const data = new FormData(form)
      context.navigate(`/bookings?date=${data.get('date')}&roomId=${data.get('roomId')}&view=${view}`)
    })
    context.root.querySelectorAll<HTMLButtonElement>('[data-view]').forEach((button) => button.addEventListener('click', () => {
      context.navigate(`/bookings?date=${date}&roomId=${roomId}&view=${button.dataset.view}`)
    }))
  } catch (caught) {
    context.root.innerHTML = pageShell('預約瀏覽', `<div class="state error">${escapeHtml(errorMessage(caught))}<button data-action="retry">重試</button></div>`, user)
  }
}

function renderBookings(bookings: Booking[], view: 'calendar' | 'list'): string {
  if (!bookings.length) return emptyState(`所選日期沒有預約（${view === 'calendar' ? '日曆' : '列表'}檢視）`, { href: '/bookings/new', label: '建立預約' })
  if (view === 'list') {
    return `<div class="table-wrap"><table><thead><tr><th>會議室</th><th>時段</th><th>用途</th><th>預約者</th></tr></thead><tbody>
      ${bookings.map((booking) => `<tr><td>${escapeHtml(booking.room?.name ?? booking.room_id)}</td><td>${formatTaipeiDateTime(booking.starts_at)}–${formatTaipeiDateTime(booking.ends_at)}</td><td>${escapeHtml(booking.purpose)}</td><td>${escapeHtml(booking.booked_by?.display_name ?? '—')}</td></tr>`).join('')}
    </tbody></table></div>`
  }
  const grouped = new Map<string, { roomName: string; bookings: Booking[] }>()
  bookings.forEach((booking) => {
    const group = grouped.get(booking.room_id)
    grouped.set(booking.room_id, {
      roomName: booking.room?.name ?? booking.room_id,
      bookings: [...(group?.bookings ?? []), booking],
    })
  })
  return `<section class="calendar" aria-label="09:00 至 21:00 預約日曆">
    <div class="calendar-hours"><span></span><div class="calendar-scale">${Array.from({ length: 13 }, (_, index) => `<span style="left:${(index / 12) * 100}%">${String(index + 9).padStart(2, '0')}:00</span>`).join('')}</div></div>
    ${Array.from(grouped.values(), ({ roomName, bookings: roomBookings }) => `<div class="calendar-row">
      <strong class="calendar-room">${escapeHtml(roomName)}</strong>
      <div class="calendar-track">
        ${roomBookings.map(calendarEvent).join('')}
      </div>
    </div>`).join('')}
  </section>`
}

function calendarEvent(booking: Booking): string {
  const startMinutes = taipeiTimeMinutes(booking.starts_at)
  const endMinutes = taipeiTimeMinutes(booking.ends_at)
  const left = Math.max(0, Math.min(100, ((startMinutes - 540) / 720) * 100))
  const width = Math.max(1, Math.min(100 - left, ((endMinutes - startMinutes) / 720) * 100))
  return `<article class="calendar-event" data-start-minute="${startMinutes}" style="left:${left}%;width:${width}%">
    <strong>${escapeHtml(booking.purpose)}</strong>
    <span>${formatTaipeiDateTime(booking.starts_at)}–${formatTaipeiDateTime(booking.ends_at)}</span>
  </article>`
}
