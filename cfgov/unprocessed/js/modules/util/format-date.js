'use strict';

/**
 * Returns a string representing the year and month based on a given integer,
  where month 0 starts at January 1st 2000, month 1 is February 1st 2000, etc.
 *
 * @param {Number} index - used to represent the month and year in the data
  sets, e.g., 0
 * @returns {String} date - formatted as Year-Month-Day, e.g., 2000-January-01
 */
function translate( index ) {
  var year = Math.floor( index / 12 ) + 2000;
  var month = index % 12;
  month += 1;
  if ( month < 10 ) {
    month = '0' + month;
  }

  return year + '-' + month + '-01';
}

module.exports = translate;
