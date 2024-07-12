/**
 * Returns an object with the UTC timestamp number in milliseconds
 * and human-friendly month and year for a given date in either format.
 * @param {number|string} date -
 *   UTC timestamp in milliseconds representing the month
 *   and year for a given data point, e.g. 1477958400000,
 *   OR a string in Month + YYYY format for a given data point,
 *   e.g. "January 2000".
 * @returns {object}
 *   Object with UTC timestamp in milliseconds and the human-readable version
 *   of the month and year for the given date.
 */
function convertDate(date) {
  let humanFriendly = null;
  let timestamp = null;
  let month = null;
  let year = null;
  const months = [
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
    'December',
  ];

  if (
    typeof date === 'number' &&
    date.toString().length >= 12 &&
    date.toString().length <= 13
  ) {
    month = new Date(date).getUTCMonth();
    month = months[month];
    year = new Date(date).getUTCFullYear();

    humanFriendly = month + ' ' + year;
    timestamp = date;
  } else if (typeof date === 'string') {
    const strLength = date.length;
    const monthString = date.substring(0, strLength - 5);

    month = months.indexOf(monthString);
    year = date.slice(date.length - 4, date.length);

    timestamp = Date.UTC(year, month, 1, 0, 0, 0, 0);
    humanFriendly = date;
  } else {
    // return error
  }

  return {
    humanFriendly: humanFriendly,
    timestamp: timestamp,
  };
}

/**
 * Get the first value that is a Number.
 * TODO: Returned value should be consistent.
 * Refactor to return null when no number is found.
 * Also, check the structure of array to fit with expections and
 * throw error if it is wrong.
 * @param {Array} array - An array of Objects with values to check.
 * @returns {string} an actual Number, or false if none was found.
 */
function getFirstNumber(array) {
  let val;
  for (let x = 0, len = array.length; x < len; x++) {
    if (!isNaN(array[x][1])) {
      val = array[x][1];
      return val;
    }
  }
  return false;
}

export { convertDate, getFirstNumber };
