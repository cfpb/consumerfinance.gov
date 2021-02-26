/**
 * @param {number} totalSeconds - The time in seconds.
 * @returns {string} Time in the HH:MM:SS format.
 */
function formatTimestamp( totalSeconds ) {
  let hours = Math.floor( totalSeconds / 3600 );
  let minutes = Math.floor( ( totalSeconds - ( hours * 3600 ) ) / 60 );
  let seconds = totalSeconds - ( hours * 3600 ) - ( minutes * 60 );

  let timestamp = '';
  if ( hours < 10 ) {
    hours = '0' + hours;
  }
  if ( hours !== '00' ) {
    timestamp = hours + ':';
  }

  if ( minutes < 10 ) {
    minutes = '0' + minutes;
  }

  if ( seconds < 10 ) {
    seconds = '0' + seconds;
  }

  timestamp += minutes + ':' + seconds;

  return timestamp;
}

/**
 * Escapes a string.
 * @param   {string} s The string to escape.
 * @returns {string}   The escaped string.
 */
function stringEscape( s ) {
  return s.replace( /[-\\^$*+?.()|[\]{}]/g, '\\$&' );
}

/**
 * Tests whether a string matches another.
 * @param   {string}  x The control string.
 * @param   {string}  y The comparison string.
 * @returns {boolean}   True if `x` and `y` match, false otherwise.
 */
function stringMatch( x, y ) {
  return RegExp( stringEscape( y.trim() ), 'i' ).test( x );
}

export {
  formatTimestamp,
  stringEscape,
  stringMatch
};
