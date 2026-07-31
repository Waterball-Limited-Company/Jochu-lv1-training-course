import type { User } from '../api/types'

export function pageShell(title: string, content: string, user?: User): string {
  return `
    <header class="topbar">
      <a class="brand" href="/home" data-link>會議室預約</a>
      ${user ? navigation(user) : ''}
    </header>
    <main class="container">
      <div class="page-heading"><div><p class="eyebrow">Asia/Taipei</p><h1>${escapeHtml(title)}</h1></div>
      ${user ? `<span class="user-chip">${escapeHtml(user.display_name)} · ${roleName(user.role)}</span>` : ''}</div>
      ${content}
    </main>`
}

export function navigation(user: User): string {
  return `<nav aria-label="主要導覽">
    <a href="/home" data-link>首頁</a>
    <a href="/bookings" data-link>預約瀏覽</a>
    <a href="/bookings/new" data-link>建立預約</a>
    <a href="/my-bookings" data-link>我的預約</a>
    ${user.role === 'facility_admin' ? '<a href="/admin/rooms" data-link>會議室管理</a>' : ''}
    <button class="link-button" type="button" data-action="logout">登出</button>
  </nav>`
}

export function loading(label = '載入中…'): string {
  return `<div class="state loading" role="status">${escapeHtml(label)}</div>`
}

export function emptyState(message: string, action?: { href: string; label: string }): string {
  return `<div class="state empty"><p>${escapeHtml(message)}</p>${action ? `<a class="button" href="${action.href}" data-link>${escapeHtml(action.label)}</a>` : ''}</div>`
}

export function errorState(message: string): string {
  return `<div class="state error" role="alert"><p>${escapeHtml(message)}</p><button type="button" data-action="retry">重試</button></div>`
}

export function statusBadge(status: string): string {
  const label = status === 'confirmed' ? '已確認' : status === 'cancelled' ? '已取消' : status
  return `<span class="badge ${escapeHtml(status)}">${escapeHtml(label)}</span>`
}

export function escapeHtml(value: unknown): string {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;')
}

function roleName(role: User['role']): string {
  return role === 'facility_admin' ? '設施管理員' : role === 'manager' ? '主管' : '員工'
}
