const TAIPEI_OFFSET = '+08:00'

export function todayInTaipei(now = new Date()): string {
  return new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Asia/Taipei',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(now)
}

export function toTaipeiIso(date: string, time: string): string {
  return `${date}T${time}:00${TAIPEI_OFFSET}`
}

export function formatTaipeiDateTime(value: string): string {
  return new Intl.DateTimeFormat('zh-TW', {
    timeZone: 'Asia/Taipei',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  }).format(new Date(value))
}

export function taipeiTimeMinutes(value: string): number {
  const parts = new Intl.DateTimeFormat('en-GB', {
    timeZone: 'Asia/Taipei',
    hour: '2-digit',
    minute: '2-digit',
    hourCycle: 'h23',
  }).formatToParts(new Date(value))
  const hours = Number(parts.find((part) => part.type === 'hour')?.value ?? 0)
  const minutes = Number(parts.find((part) => part.type === 'minute')?.value ?? 0)
  return hours * 60 + minutes
}

export function validateBookingWindow(date: string, start: string, end: string): string | null {
  if (!date || !start || !end) return '請填寫日期、開始與結束時間'
  const day = new Date(`${date}T12:00:00${TAIPEI_OFFSET}`).getUTCDay()
  if (day === 0 || day === 6) return '僅可預約平日'
  const startMinutes = toMinutes(start)
  const endMinutes = toMinutes(end)
  if (endMinutes <= startMinutes) return '結束時間必須晚於開始時間'
  if (startMinutes < 9 * 60 || endMinutes > 21 * 60) return '預約須在 09:00–21:00 之間'
  const duration = endMinutes - startMinutes
  if (duration < 30) return '預約至少需要 30 分鐘'
  if (duration > 240) return '預約最長為 4 小時'
  return null
}

function toMinutes(value: string): number {
  const [hours = 0, minutes = 0] = value.split(':').map(Number)
  return hours * 60 + minutes
}
