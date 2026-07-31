import { afterEach, beforeEach, vi } from 'vitest'
import { setApiBaseUrl, useMockApi } from '../../src/api/client'
import { clearSession } from '../../src/auth/session'

beforeEach(() => {
  document.body.innerHTML = '<div id="app"></div>'
  history.replaceState({}, '', '/login')
  sessionStorage.clear()
  localStorage.clear()
  clearSession()
  useMockApi(false)
  vi.spyOn(window, 'confirm').mockReturnValue(true)
})

afterEach(() => {
  setApiBaseUrl('')
  document.body.innerHTML = ''
})
