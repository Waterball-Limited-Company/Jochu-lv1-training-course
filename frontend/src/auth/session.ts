import { apiRequest } from '../api/client'
import type { User } from '../api/types'

let currentUser: User | null = null

export async function loadSession(): Promise<User> {
  const response = await apiRequest<{ authenticated: true; user: User }>('/api/auth/me')
  currentUser = response.user
  return response.user
}

export async function login(username: string, password: string): Promise<User> {
  const response = await apiRequest<{ authenticated: true; user: User }>('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  })
  currentUser = response.user
  return response.user
}

export async function logout(): Promise<void> {
  await apiRequest('/api/auth/logout', { method: 'POST' })
  currentUser = null
}

export function getCurrentUser(): User | null {
  return currentUser
}

export function clearSession(): void {
  currentUser = null
}
