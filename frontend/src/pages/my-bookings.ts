import { apiRequest, errorMessage } from '../api/client'
import type { Booking } from '../api/types'
import { emptyState, escapeHtml, pageShell, statusBadge } from '../components/ui'
import { formatTaipeiDateTime } from '../lib/datetime-taipei'
import type { PageContext } from '../router'

export async function renderMyBookings(context: PageContext): Promise<void> {
  const user = await context.requireUser()
  if (!user) return
  try {
    const response = await apiRequest<{ bookings: Booking[] }>('/api/bookings/mine')
    const flash = sessionStorage.getItem('booking-flash')
    sessionStorage.removeItem('booking-flash')
    const content = response.bookings.length
      ? `<section class="booking-list">${response.bookings.map(bookingCard).join('')}</section>`
      : emptyState('你目前沒有任何預約', { href: '/bookings/new', label: '建立第一筆預約' })
    context.root.innerHTML = pageShell('我的預約', `${flash ? `<p class="flash" role="status">${escapeHtml(flash)}</p>` : ''}<div data-cancel-error class="form-error"></div>${content}`, user)
    bindCancel(context)
  } catch (caught) {
    context.root.innerHTML = pageShell('我的預約', `<div class="state error">${escapeHtml(errorMessage(caught))}<button data-action="retry">重試</button></div>`, user)
  }
}

function bookingCard(booking: Booking): string {
  return `<article class="card booking-card" data-booking-id="${booking.id}">
    <div class="card-title"><h2>${escapeHtml(booking.room?.name ?? booking.room_id)}</h2>${statusBadge(booking.status)}</div>
    <p>${escapeHtml(booking.room?.floor ?? '')} · ${formatTaipeiDateTime(booking.starts_at)}–${formatTaipeiDateTime(booking.ends_at)}</p>
    <p><strong>${escapeHtml(booking.purpose)}</strong> · ${booking.attendee_count} 人</p>
    <p>${booking.needs_projector ? '需要投影機' : '不需投影機'} · ${booking.needs_video_conference ? '需要視訊' : '不需視訊'}</p>
    ${booking.is_cancellable ? `<button type="button" class="danger" data-cancel="${booking.id}">取消預約</button>` : '<span class="muted">此預約已不可取消</span>'}
  </article>`
}

function bindCancel(context: PageContext): void {
  context.root.querySelectorAll<HTMLButtonElement>('[data-cancel]').forEach((button) => button.addEventListener('click', async () => {
    if (!window.confirm('確定取消這筆預約？取消後時段將釋放。')) return
    button.disabled = true
    try {
      const booking = await apiRequest<Booking>(`/api/bookings/${button.dataset.cancel}/cancel`, { method: 'POST' })
      const card = button.closest<HTMLElement>('[data-booking-id]')!
      card.querySelector('.badge')!.outerHTML = statusBadge(booking.status)
      button.outerHTML = '<span class="muted">此預約已不可取消</span>'
    } catch (caught) {
      context.root.querySelector<HTMLElement>('[data-cancel-error]')!.textContent = errorMessage(caught)
      button.disabled = false
    }
  }))
}
