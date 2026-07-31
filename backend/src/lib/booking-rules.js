import { getTaipeiParts } from './time.js';

export function obeysBookingRules(startsAt, endsAt) {
  const start = getTaipeiParts(startsAt);
  const end = getTaipeiParts(endsAt);
  const durationMinutes = (endsAt.getTime() - startsAt.getTime()) / 60_000;
  const endsAfterClosing =
    end.minutes > 21 * 60 ||
    (end.minutes === 21 * 60 && (end.seconds > 0 || endsAt.getMilliseconds() > 0));
  return (
    start.date === end.date &&
    !['Sat', 'Sun'].includes(start.weekday) &&
    start.minutes >= 9 * 60 &&
    !endsAfterClosing &&
    durationMinutes >= 30 &&
    durationMinutes <= 240
  );
}
