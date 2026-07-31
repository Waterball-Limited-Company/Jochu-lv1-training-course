import { apiRequest, errorMessage } from '../api/client'
import type { MaintenanceWindow, Room } from '../api/types'
import { emptyState, escapeHtml, pageShell } from '../components/ui'
import { formatTaipeiDateTime, toTaipeiIso, todayInTaipei } from '../lib/datetime-taipei'
import type { PageContext } from '../router'

export async function renderAdminRooms(context: PageContext): Promise<void> {
  const user = await context.requireUser()
  if (!user) return
  if (user.role !== 'facility_admin') {
    context.root.innerHTML = pageShell('無權存取', `<div class="state error"><p>只有設施管理員可管理會議室。</p><a class="button" href="/home" data-link>返回首頁</a></div>`, user)
    return
  }
  try {
    const response = await apiRequest<{ rooms: Room[] }>('/api/rooms')
    context.root.innerHTML = pageShell('會議室管理', `
      <div class="admin-layout">
        <section>
          <div class="section-heading"><h2>全部會議室</h2></div>
          ${response.rooms.length ? `<div class="grid">${response.rooms.map(roomAdminCard).join('')}</div>` : emptyState('目前沒有會議室')}
        </section>
        <aside class="stack">
          ${createRoomForm()}
          ${maintenanceForm(response.rooms)}
        </aside>
      </div>
      <p class="form-error" data-admin-error aria-live="polite"></p>`, user)
    bindAdmin(context)
  } catch (caught) {
    context.root.innerHTML = pageShell('會議室管理', `<div class="state error">${escapeHtml(errorMessage(caught))}<button data-action="retry">重試</button></div>`, user)
  }
}

function roomAdminCard(room: Room): string {
  return `<article class="card" data-admin-room="${room.id}">
    <div class="card-title"><h3>${escapeHtml(room.name)}</h3><span class="badge ${room.is_active ? 'active' : 'inactive'}">${room.is_active ? '啟用中' : '已停用'}</span></div>
    <p>${escapeHtml(room.floor)} · ${room.capacity} 人</p>
    ${room.is_active ? `<button class="danger" type="button" data-deactivate="${room.id}">停用</button><p class="hint">只阻擋新預約，不取消既有已確認預約。</p>` : '<span class="muted">不可接受新預約</span>'}
  </article>`
}

function createRoomForm(): string {
  return `<section class="card"><h2>新增會議室</h2><form id="room-form">
    <label>名稱<input name="name" required></label><label>樓層<input name="floor" required></label>
    <label>容量<input name="capacity" type="number" min="1" required></label>
    <label class="check"><input name="has_projector" type="checkbox">投影機</label>
    <label class="check"><input name="has_video_conference" type="checkbox">視訊設備</label>
    <button type="submit">新增</button>
  </form></section>`
}

function maintenanceForm(rooms: Room[]): string {
  const today = todayInTaipei()
  return `<section class="card"><h2>新增維護時段</h2><form id="maintenance-form">
    <label>會議室<select name="room_id">${rooms.map((room) => `<option value="${room.id}">${escapeHtml(room.name)}</option>`).join('')}</select></label>
    <label>日期<input name="date" type="date" value="${today}" required></label>
    <label>開始<input name="start" type="time" value="10:00" required></label>
    <label>結束<input name="end" type="time" value="12:00" required></label>
    <label>說明<input name="note"></label><div data-maintenance-list></div>
    <button type="submit">建立維護時段</button>
  </form></section>`
}

function bindAdmin(context: PageContext): void {
  const showError = (caught: unknown): void => {
    context.root.querySelector<HTMLElement>('[data-admin-error]')!.textContent = errorMessage(caught)
  }
  context.root.querySelector<HTMLFormElement>('#room-form')?.addEventListener('submit', async (event) => {
    event.preventDefault()
    const data = new FormData(event.currentTarget as HTMLFormElement)
    try {
      await apiRequest('/api/rooms', { method: 'POST', body: JSON.stringify({
        name: data.get('name'), floor: data.get('floor'), capacity: Number(data.get('capacity')),
        has_projector: data.get('has_projector') === 'on', has_video_conference: data.get('has_video_conference') === 'on',
      }) })
      await context.refresh()
    } catch (caught) { showError(caught) }
  })
  context.root.querySelectorAll<HTMLButtonElement>('[data-deactivate]').forEach((button) => button.addEventListener('click', async () => {
    if (!window.confirm('停用只阻擋新預約，不取消既有預約。確定停用？')) return
    try {
      await apiRequest(`/api/rooms/${button.dataset.deactivate}`, { method: 'PATCH', body: JSON.stringify({ is_active: false }) })
      await context.refresh()
    } catch (caught) { showError(caught) }
  }))
  const form = context.root.querySelector<HTMLFormElement>('#maintenance-form')
  const loadWindows = async (): Promise<void> => {
    if (!form) return
    const data = new FormData(form)
    const date = String(data.get('date'))
    try {
      const response = await apiRequest<{ maintenance_windows: MaintenanceWindow[] }>(`/api/rooms/${data.get('room_id')}/maintenance-windows?from=${encodeURIComponent(toTaipeiIso(date, '00:00'))}&to=${encodeURIComponent(toTaipeiIso(date, '23:59'))}`)
      form.querySelector<HTMLElement>('[data-maintenance-list]')!.innerHTML = response.maintenance_windows.length
        ? response.maintenance_windows.map((item) => `<p class="hint">${formatTaipeiDateTime(item.starts_at)}–${formatTaipeiDateTime(item.ends_at)} ${escapeHtml(item.note ?? '')}</p>`).join('')
        : '<p class="hint">此區間沒有維護時段</p>'
    } catch (caught) { showError(caught) }
  }
  form?.addEventListener('change', () => void loadWindows())
  form?.addEventListener('submit', async (event) => {
    event.preventDefault()
    const data = new FormData(form)
    const start = String(data.get('start'))
    const end = String(data.get('end'))
    if (end <= start) {
      showError(new Error('結束時間必須晚於開始時間'))
      context.root.querySelector<HTMLElement>('[data-admin-error]')!.textContent = '結束時間必須晚於開始時間'
      return
    }
    try {
      await apiRequest(`/api/rooms/${data.get('room_id')}/maintenance-windows`, {
        method: 'POST',
        body: JSON.stringify({ starts_at: toTaipeiIso(String(data.get('date')), start), ends_at: toTaipeiIso(String(data.get('date')), end), note: data.get('note') }),
      })
      await loadWindows()
    } catch (caught) { showError(caught) }
  })
  void loadWindows()
}
