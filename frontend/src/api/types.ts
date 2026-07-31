export type Role = 'employee' | 'manager' | 'facility_admin'

export interface User {
  id: string
  username: string
  display_name: string
  role: Role
  created_at: string
}

export interface Room {
  id: string
  name: string
  floor: string
  capacity: number
  has_projector: boolean
  has_video_conference: boolean
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface Booking {
  id: string
  room_id: string
  user_id: string
  room?: Pick<Room, 'name' | 'floor'>
  booked_by?: { display_name: string }
  purpose: string
  attendee_count: number
  needs_projector: boolean
  needs_video_conference: boolean
  starts_at: string
  ends_at: string
  status: 'confirmed' | 'cancelled'
  is_cancellable?: boolean
  created_at: string
  updated_at: string
}

export interface MaintenanceWindow {
  id: string
  room_id: string
  starts_at: string
  ends_at: string
  note: string | null
  created_by: string
  created_at: string
}

export interface ApiErrorShape {
  error: {
    code: string
    message: string
    details: Array<Record<string, unknown>>
  }
}

export interface OverviewRoom {
  room_id: string
  room_name: string
  is_active: boolean
  booked_minutes: number
  business_minutes: number
  busy_ratio: number
  confirmed_booking_count: number
}
