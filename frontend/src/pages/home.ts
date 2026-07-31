import { apiRequest, errorMessage } from '../api/client'
import type { OverviewRoom, Room } from '../api/types'
import { emptyState, escapeHtml, pageShell } from '../components/ui'
import type { PageContext } from '../router'

export async function renderHome(context: PageContext): Promise<void> {
  const user = await context.requireUser()
  if (!user) return
  try {
    const [roomResponse, overview] = await Promise.all([
      apiRequest<{ rooms: Room[] }>('/api/rooms'),
      apiRequest<{ date: string; timezone: string; rooms: OverviewRoom[] }>('/api/overview/today'),
    ])
    const summaries = new Map(overview.rooms.map((item) => [item.room_id, item]))
    const roomCards = roomResponse.rooms.length ? roomResponse.rooms.map((room) => {
      const summary = summaries.get(room.id)
      const empty = !summary?.confirmed_booking_count
      return `<article class="card room-card ${room.is_active ? '' : 'inactive'}" data-room-id="${room.id}">
        <div class="card-title"><h2>${escapeHtml(room.name)}</h2><span class="badge ${room.is_active ? 'active' : 'inactive'}">${room.is_active ? '啟用中' : '已停用・不可新約'}</span></div>
        <p>${escapeHtml(room.floor)} · ${room.capacity} 人 · ${room.has_projector ? '有投影機' : '無投影機'} · ${room.has_video_conference ? '有視訊' : '無視訊'}</p>
        <div class="busy"><strong>${empty ? '今日皆空閒' : `忙碌 ${Math.round((summary?.busy_ratio ?? 0) * 100)}%`}</strong>
          <span>${summary?.confirmed_booking_count ?? 0} 筆／${summary?.booked_minutes ?? 0} 分鐘</span></div>
        ${room.is_active ? `<a class="button" href="/bookings/new?roomId=${room.id}" data-link>預約此會議室</a>` : '<span class="muted">此會議室不接受新預約</span>'}
      </article>`
    }).join('') : emptyState('目前沒有會議室')
    context.root.innerHTML = pageShell('今日會議室概況', `
      <p class="lead">${escapeHtml(overview.date)} · ${escapeHtml(overview.timezone)}，快速掌握忙碌程度並開始預約。</p>
      <section class="grid rooms">${roomCards}</section>`, user)
  } catch (caught) {
    context.root.innerHTML = pageShell('今日會議室概況', `<div class="state error" role="alert">${escapeHtml(errorMessage(caught))}<button data-action="retry">重試</button></div>`, user)
  }
}
