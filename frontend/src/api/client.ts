import { MockApiError, mockRequest } from './mock'
import type { ApiErrorShape } from './types'

export class ApiError extends Error {
  status: number
  code: string
  details: Array<Record<string, unknown>>

  constructor(
    status: number,
    code: string,
    message: string,
    details: Array<Record<string, unknown>> = [],
  ) {
    super(message)
    this.status = status
    this.code = code
    this.details = details
  }
}

let mockEnabled = import.meta.env.VITE_USE_MOCK === 'true'
let apiBaseUrl = ''
let unauthorizedHandler: (() => void) | null = null

export function useMockApi(enabled: boolean): void {
  mockEnabled = enabled
}

export function setApiBaseUrl(baseUrl: string): void {
  apiBaseUrl = baseUrl.replace(/\/$/, '')
}

export function onUnauthorized(handler: () => void): void {
  unauthorizedHandler = handler
}

export async function apiRequest<T>(path: string, init: RequestInit = {}): Promise<T> {
  try {
    if (mockEnabled) return await mockRequest<T>(path, init)
    const headers = new Headers(init.headers)
    if (init.body && !headers.has('Content-Type')) headers.set('Content-Type', 'application/json')
    const response = await fetch(`${apiBaseUrl}${path}`, { ...init, headers, credentials: 'include' })
    const data = await response.json() as T | ApiErrorShape
    if (!response.ok) {
      const payload = data as ApiErrorShape
      throw new ApiError(response.status, payload.error.code, payload.error.message, payload.error.details)
    }
    return data as T
  } catch (caught) {
    const error = caught instanceof MockApiError
      ? new ApiError(caught.status, caught.code, caught.message, caught.details)
      : caught
    if (error instanceof ApiError && error.status === 401) unauthorizedHandler?.()
    throw error
  }
}

export function errorMessage(caught: unknown): string {
  if (!(caught instanceof ApiError)) return '發生未預期錯誤，請稍後重試'
  const messages: Record<string, string> = {
    INVALID_CREDENTIALS: '帳號或密碼錯誤',
    BOOKING_CONFLICT: '該時段已有預約，請調整時間',
    MAINTENANCE_CONFLICT: '該時段因維護而不可預約',
    BOOKING_RULE_VIOLATION: caught.message,
    BOOKING_NOT_CANCELLABLE: '此預約已結束或取消，無法再次取消',
    FORBIDDEN: '您沒有權限執行此操作',
  }
  return messages[caught.code] ?? caught.message
}
