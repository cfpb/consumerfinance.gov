import { DateTime, Info } from 'luxon';

/**
 * Luxon's DateTime class
 * @external DateTime
 * @see {@link https://moment.github.io/luxon/docs/class/src/datetime.js~DateTime.html|DateTime}
 */

export const DAY_NAMES = Info.weekdays();
export const DAY_LABELS = DAY_NAMES.map((name) => name.charAt(0));
export const MONTH_NAMES = Info.months();

/**
 * Ensures that the argument is returned as a DateTime
 *
 * @param {Date|DateTime} date - A Date instance or DateTime object
 * @returns {DateTime} a Luxon DateTime instance
 */
export const toDateTime = (date) => DateTime.isDateTime(date) ? date : DateTime.fromJSDate(date);

/**
 * Returns the number of the specified month, zero-indexed.
 *
 * @param {String} monthName - The name of the current month
 */
export const getMonthNumber = (monthName) => MONTH_NAMES.indexOf(monthName);

/**
 * Limits the number to a valid month number, zero-indexed
 *
 * @param {Number} num - The month number
 * @returns {Number} A number between 0 and 11
 */
export const limitMonthNumber = (num) => Math.min(Math.max(num, 0), 11);

/**
 * An object containing information about a month
 * @typedef {Object} MonthInfo
 * @property {Number} firstWeekDay - The weekday number of the first day of the month
 * @property {Number} daysInMonth - The number of days in the month
 */

/**
 * Returns the number of the first day of the specified date's month, and the total number of days the month has
 *
 * @param {Date|DateTime} date - A JS Date or Luxon DateTime instance
 * @returns {Object}
 */
export function getMonthInfo(date = DateTime.local()) {
  date = toDateTime(date);
  const firstWeekDay = date.startOf('month').get('weekday');
  const daysInMonth = date.endOf('month').get('day');
  return { firstWeekDay, daysInMonth };
}

/**
 * An object representing a week row on the calendar
 * @typedef {Object} Week
 * @property {DateTime[]} days - An array of DateTime objects, one for each day of the week
 * @property {Number} weekNumber - The week number of the year
 */

/**
 * Get an array of objects representing weeks of the month, containing the week number and an array of weekdays
 *
 * @param {DateTime|Date} date - A reference date representing the current or selected month
 * @returns {Week[]} An array of Week objects
 */
export function getWeekRows(date) {
  date = toDateTime(date);
  const startWeek = date.startOf('month').get('weekNumber');
  const endWeek = date.endOf('month').get('weekNumber') + 1;
  const rows = [];

  for (let weekNumber = startWeek; weekNumber < endWeek; weekNumber++) {
    const startOfWeek = date.set({ weekNumber }).startOf('week');

    rows.push({
      weekNumber,
      days: Array(7).fill(0).map((n, i) => startOfWeek.plus({ days: n + i })),
    });
  }

  return rows;
}
