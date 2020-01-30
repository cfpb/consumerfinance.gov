import { DateTime, Info } from 'luxon';

export const DAY_NAMES = Info.weekdays();
export const DAY_LABELS = DAY_NAMES.map((name) => name.charAt(0));
export const MONTH_NAMES = Info.months();

export function getMonthNumber(month) {
  return MONTH_NAMES.indexOf(month);
}

export function getMonthInfo(date = DateTime.local()) {
  const firstWeekDay = date.startOf('month').get('weekday');
  const daysInMonth = date.endOf('month').get('day');
  return { firstWeekDay, daysInMonth };
}
