import { afterEach, beforeEach, vi } from 'vitest'
import { resetMockApi } from '../src/api/mock'
import { useMockApi } from '../src/api/client'

beforeEach(() => {
  document.body.innerHTML = '<div id="app"></div>'
  history.replaceState({}, '', '/login')
  sessionStorage.clear()
  localStorage.clear()
  useMockApi(true)
  resetMockApi()
  vi.spyOn(window, 'confirm').mockReturnValue(true)
})

afterEach(() => {
  document.body.innerHTML = ''
})
