const taipeiDateFormatter = new Intl.DateTimeFormat('en-CA', {
  timeZone: 'Asia/Taipei',
  year: 'numeric',
  month: '2-digit',
  day: '2-digit',
});

function todayAsUtcCalendarDate() {
  return new Date(`${taipeiDateFormatter.format(new Date())}T00:00:00Z`);
}

function formatUtcCalendarDate(date) {
  return date.toISOString().slice(0, 10);
}

export function taipeiWeekdayDate(direction, ordinal = 1) {
  const date = todayAsUtcCalendarDate();
  let weekdaysSeen = 0;
  while (weekdaysSeen < ordinal) {
    date.setUTCDate(date.getUTCDate() + direction);
    const weekday = date.getUTCDay();
    if (weekday !== 0 && weekday !== 6) weekdaysSeen += 1;
  }
  return formatUtcCalendarDate(date);
}
