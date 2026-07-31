import { errorMessage } from '../api/client'
import { loadSession, login } from '../auth/session'
import { pageShell } from '../components/ui'
import type { PageContext } from '../router'

export async function renderLogin(context: PageContext): Promise<void> {
  try {
    await loadSession()
    context.navigate('/home', true)
    return
  } catch {
    context.root.innerHTML = pageShell('登入', `
      <section class="card narrow">
        <p>請使用內部帳號登入。測試帳號：alice、manager 或 admin；密碼皆為 training-password。</p>
        <form id="login-form" novalidate>
          <label>帳號<input name="username" autocomplete="username" required></label>
          <label>密碼<input name="password" type="password" autocomplete="current-password" required></label>
          <p class="form-error" data-error aria-live="polite"></p>
          <button type="submit">登入</button>
        </form>
      </section>`)
  }

  context.root.querySelector<HTMLFormElement>('#login-form')?.addEventListener('submit', async (event) => {
    event.preventDefault()
    const form = event.currentTarget as HTMLFormElement
    const data = new FormData(form)
    const username = String(data.get('username') ?? '').trim()
    const password = String(data.get('password') ?? '')
    const error = form.querySelector<HTMLElement>('[data-error]')!
    if (!username || !password) {
      error.textContent = '請填寫帳號與密碼'
      return
    }
    const button = form.querySelector<HTMLButtonElement>('button')!
    button.disabled = true
    button.textContent = '登入中…'
    try {
      await login(username, password)
      context.navigate('/home')
    } catch (caught) {
      error.textContent = errorMessage(caught)
      button.disabled = false
      button.textContent = '登入'
    }
  })
}
