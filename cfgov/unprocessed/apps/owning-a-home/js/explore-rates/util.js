import format from 'date-format';

/**
 * @param  {string} timestamp - A timestamp.
 * @return {string} Date in the format of MM/dd/yyyy.
 */
function formatTimestampMMddyyyy( timestamp ) {

  /* Should you want to format the the date for older versions of IE
     the following can be used:
     timestamp = then.slice(0, 10).replace('-', '/');
     timestamp = new Date( timestamp );
     return (timestamp.getUTCMonth() + 1) + '/' + timestamp.getUTCDate() +
            '/' +  timestamp.getUTCFullYear(); */
  return format.asString( 'MM/dd/yyyy', new Date( timestamp ) );
};

/**
 * Updates the sentence data date sentence below the chart.
 * @param {HTMLNode} elem - An HTML element holding the timestamp.
 * @param {string} time - Timestamp from API.
 */
function renderDatestamp( elem, time ) {
  elem.textContent = formatTimestampMMddyyyy( time );
}

module.exports = {
  formatTimestampMMddyyyy,
  renderDatestamp
};
