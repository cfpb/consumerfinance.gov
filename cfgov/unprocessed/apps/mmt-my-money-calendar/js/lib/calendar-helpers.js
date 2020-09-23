import dayjs from 'dayjs';
import yearDay from 'dayjs/plugin/dayOfYear';
import weekOfYear from 'dayjs/plugin/weekOfYear';
import isSameOrAfter from 'dayjs/plugin/isSameOrAfter';
import isSameOrBefore from 'dayjs/plugin/isSameOrBefore';
import isBetween from 'dayjs/plugin/isBetween';
import customParseFormat from 'dayjs/plugin/customParseFormat';
import { RRule, RRuleSet } from 'rrule';

dayjs.extend( yearDay );
dayjs.extend( weekOfYear );
dayjs.extend( customParseFormat );
dayjs.extend( isSameOrAfter );
dayjs.extend( isSameOrBefore );
dayjs.extend( isBetween );

export { dayjs };

export const DAY_NAMES = [ 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday' ];
export const DAY_LABELS = DAY_NAMES.map( name => name.charAt( 0 ) );
export const MONTH_NAMES = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December'
];

export function numberWithOrdinal( num ) {
  const suffixes = [ 'th', 'st', 'nd', 'rd' ];
  const v = num % 100;
  return num + ( suffixes[( v - 20 ) % 10] || suffixes[v] || suffixes[0] );
}

export const toDayJS = date => dayjs( date );


/** Ensures that the argument is returned as a native JS Date object
 *
 * @param {Date|dayjs} date - A JS Date or dayjs object
 * @returns {Date} a js date
 */
export const toJSDate = date => ( date instanceof Date ? date : date.toDate() );

/** Get the ordinal day of the year for a date, as an integer
 *
 * @param {Date|dayjs} date - A Date or dayjs instance
 * @returns {Number} an integer between 1 and 365
 */
export const dayOfYear = date => toDayJS( date ).dayOfYear();

/** Returns the number of the specified month, zero-indexed.
 *
 * @param {String} monthName - The name of the current month
 * @returns {Number} an index of a month
 */
export const getMonthNumber = monthName => MONTH_NAMES.indexOf( monthName );

/** Limits the number to a valid month number, zero-indexed
 *
 * @param {Number} num - The month number
 * @returns {Number} A number between 0 and 11
 */
export const limitMonthNumber = num => Math.min( Math.max( num, 0 ), 11 );

/** An object containing information about a month
 * @typedef {Object} MonthInfo
 * @property {Number} firstWeekDay - The weekday number of the first day of the month
 * @property {Number} daysInMonth - The number of days in the month
 */

/** Returns the number of the first day of the specified date's month, and the total number of days the month has
 *
 * @param {Date|dayjs} date - A JS Date or dayjs instance
 * @returns {Object} returns first day of the month and total number of days of the month
 */
export function getMonthInfo( date = dayjs() ) {
  date = toDayJS( date );
  const firstWeekDay = date.startOf( 'month' ).date();
  const daysInMonth = date.daysInMonth();
  return { firstWeekDay, daysInMonth };
}

/**
 * An object representing a week row on the calendar
 * @typedef {Object} Week
 * @property {dayjs[]} days - An array of dayjs objects, one for each day of the week
 * @property {Number} weekNumber - The week number of the year
 */

const monthSharesFirstWeek = date => {
  const start = date.startOf( 'month' );
  return start.week() === start.subtract( 1, 'month' ).endOf( 'month' ).week();
};

const monthSharesLastWeek = date => {
  const end = date.endOf( 'month' );
  return end.week() === end.add( 1, 'month' ).startOf( 'month' ).week();
};

/**
 * Get an array of objects representing weeks of the month, containing the week number and an array of weekdays
 *
 * @param {dayjs|Date} date - A reference date representing the current or selected month
 * @returns {Week[]} An array of Week objects
 */
export function getWeekRows( date ) {
  date = toDayJS( date );
  const rows = [];
  let numWeeks = Math.ceil( date.daysInMonth() / 7 );

  if ( monthSharesFirstWeek( date ) && monthSharesLastWeek( date ) ) {
    numWeeks += 1;
  }

  /* let currentWeekStart; */
  let currentWeekStart = date.startOf( 'week' );

  if ( currentWeekStart ) {
    while (
      currentWeekStart.startOf( 'week' ).isSame( date, 'month' ) ||
      currentWeekStart.endOf( 'week' ).isSame( date, 'month' )
    ) {
      const weekNumber = currentWeekStart.week();
      rows.push( {
        weekNumber,
        days: Array( 7 )
          .fill( 0 )
          /* eslint-disable-next-line */
          .map( ( n, idx ) => currentWeekStart.add( n + idx, 'days' ) )
      } );
      currentWeekStart = currentWeekStart.add( 1, 'week' );
    }
  }
  return rows;
}

export const WEEKDAYS = [ RRule.MO, RRule.TU, RRule.WE, RRule.TH, RRule.FR ];

export const DAY_OPTIONS = {
  Sunday: RRule.SU,
  Monday: RRule.MO,
  Tuesday: RRule.TU,
  Wednesday: RRule.WE,
  Thursday: RRule.TH,
  Friday: RRule.FR,
  Saturday: RRule.S
};

export const recurrenceRules = {
  weekly: {
    label: 'Weekly',
    handler: ( dtstart, options = {} ) => new RRule( { freq: RRule.WEEKLY, dtstart, ...options } )
  },
  biweekly: {
    label: 'Every 2 weeks',
    handler: ( dtstart, options = {} ) => new RRule( {
      freq: RRule.WEEKLY,
      interval: 2,
      dtstart,
      ...options
    } )
  },
  monthly: {
    label: 'Monthly',
    handler: ( dtstart, options = {} ) => new RRule( { freq: RRule.MONTHLY, dtstart, ...options } )
  },
  semimonthly: {
    label: 'Twice a month',
    handler: ( dtstart, payday1 = 15, payday2 = 30 ) => {
      const rules = new RRuleSet();

      const firstPaydayRange = [ 0, 1, 2 ].map( num => ( payday1 > 2 ? payday1 - num : payday1 + num ) ).sort();
      const lastPaydayRange =
        payday2 > 29 ? null : [ 0, 1, 2 ].map( num => ( payday2 > 2 ? payday2 - num : payday2 + num ) ).sort();

      // The last business day before the first payday provided, not considering holidays:
      rules.rrule(
        new RRule( {
          dtstart,
          freq: RRule.MONTHLY,
          bysetpos: -1,
          byweekday: WEEKDAYS,
          bymonthday: firstPaydayRange
        } )
      );

      // The last business day of the month:
      rules.rrule(
        new RRule( {
          freq: RRule.MONTHLY,
          bysetpos: -1,
          byweekday: WEEKDAYS,
          bymonthday: lastPaydayRange
        } )
      );

      return rules;
    }
  }
};
