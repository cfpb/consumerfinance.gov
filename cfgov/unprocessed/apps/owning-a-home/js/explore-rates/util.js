import formatDate from 'date-format';
import formatUSD from 'format-usd';
import unFormatUSD from 'unformat-usd';

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
  return formatDate.asString( 'MM/dd/yyyy', new Date( timestamp ) );
};

/**
 * Updates the sentence data date sentence below the chart.
 * @param {HTMLNode} elem - An HTML element holding the timestamp.
 * @param {string} time - Timestamp from API.
 */
function renderDatestamp( elem, time ) {
  elem.textContent = formatTimestampMMddyyyy( time );
}

/**
 * Calculate and render the loan amount.
 */
function calcLoanAmount( housePrice, downPayment ) {
  const loan = unFormatUSD( housePrice ) - unFormatUSD( downPayment );

  if ( loan > 0 ) {
    return loan;
  }

  return 0;
}

/**
 * Calculate and render the loan amount.
 */
function renderLoanAmount( elem, loanAmount ) {
  elem.textContent = formatUSD( loanAmount, { decimalPlaces: 0 } );
}

module.exports = {
  calcLoanAmount,
  formatTimestampMMddyyyy,
  renderDatestamp,
  renderLoanAmount
};
