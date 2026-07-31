import { onUnauthorized } from './api/client'
import type { User } from './api/types'
import { clearSession, loadSession, logout } from './auth/session'
import { escapeHtml, loading } from './components/ui'
import { renderAdminRooms } from './pages/admin-rooms'
import { renderBookingCreate } from './pages/booking-create'
import { renderBookingsBrowse } from './pages/bookings-browse'
import { renderHome } from './pages/home'
import { renderLogin } from './pages/login'
import { renderMyBookings } from './pages/my-bookings'

export interface PageContext {
  root: HTMLElement
  navigate: (url: string, replace?: boolean) => void
  refresh: () => Promise<void>
  requireUser: () => Promise<User | null>
}

type PageRenderer = (context: PageContext) => Promise<void>

const routes: Record<string, PageRenderer> = {
  '/login': renderLogin,
  '/home': renderHome,
  '/bookings': renderBookingsBrowse,
  '/bookings/new': renderBookingCreate,
  '/my-bookings': renderMyBookings,
  '/admin/rooms': renderAdminRooms,
}

export function createRouter(root: HTMLElement): { render: () => Promise<void>; navigate: PageContext['navigate'] } {
  let renderVersion = 0
  const navigate = (url: string, replace = false): void => {
    if (replace) history.replaceState({}, '', url)
    else history.pushState({}, '', url)
    void render()
  }
  const render = async (): Promise<void> => {
    const version = ++renderVersion
    const renderer = routes[location.pathname]
    if (!renderer) {
      navigate('/home', true)
      return
    }
    root.innerHTML = loading()
    const stagingRoot = document.createElement('div')
    const context: PageContext = {
      root: stagingRoot,
      navigate,
      refresh: () => render(),
      requireUser: async () => {
        try {
          return await loadSession()
        } catch {
          if (location.pathname !== '/login') navigate('/login', true)
          return null
        }
      },
    }
    try {
      await renderer(context)
      if (version !== renderVersion) return
      root.replaceChildren(...stagingRoot.childNodes)
      context.root = root
    } catch (caught) {
      if (version !== renderVersion) return
      const message = caught instanceof Error ? caught.message : '未知錯誤'
      root.innerHTML = `<main class="container"><div class="state error" role="alert">頁面載入失敗：${escapeHtml(message)}<button data-action="retry">重試</button></div></main>`
    }
  }

  root.addEventListener('click', (event) => {
    const target = event.target as Element
    const link = target.closest<HTMLAnchorElement>('a[data-link]')
    if (link) {
      event.preventDefault()
      navigate(`${link.pathname}${link.search}`)
      return
    }
    if (target.closest('[data-action="retry"]')) void render()
    if (target.closest('[data-action="logout"]')) {
      void logout().finally(() => {
        clearSession()
        navigate('/login')
      })
    }
  })
  window.addEventListener('popstate', () => void render())
  onUnauthorized(() => {
    clearSession()
    if (location.pathname !== '/login') navigate('/login', true)
  })
  return { render, navigate }
}
