import formatDate from 'date-format';
import formatUSD from 'format-usd';
import unFormatUSD from 'unformat-usd';

/**
 * Simple (anonymous) delay function.
 * @return {Object} function that has been delayed.
 */
const delay = ( function() {
  let t = 0;
  return function( callback, delayAmount ) {
    clearTimeout( t );
    t = setTimeout( callback, delayAmount );
  };
} )();

/**
 * @param  {string} timestamp - A timestamp.
 * @returns {string} Date in the format of MM/dd/yyyy.
 */
function formatTimestampMMddyyyy( timestamp ) {

  /* Should you want to format the the date for older versions of IE
     the following can be used:
     timestamp = then.slice(0, 10).replace('-', '/');
     timestamp = new Date( timestamp );
     return (timestamp.getUTCMonth() + 1) + '/' + timestamp.getUTCDate() +
            '/' +  timestamp.getUTCFullYear(); */
  return formatDate.asString( 'MM/dd/yyyy', new Date( timestamp ) );
}

/**
 * Render chart data in an accessible format.
 * @param {HTMLNode} tableHead - A <thead> element.
 * @param {HTMLNode} tableBody - A <tbody> element.
 * @param {Array} labels - Data labels from the API.
 * @param {Array} vals - Data values from the API.
 */
function renderAccessibleData( tableHead, tableBody, labels, vals ) {
  // Empty the contents of the table elements (equivalent to jQuery's .empty()).
  while ( tableHead.firstChild ) tableHead.removeChild( tableHead.firstChild );
  while ( tableBody.firstChild ) tableBody.removeChild( tableBody.firstChild );

  labels.forEach( value => {
    const thElem = document.createElement( 'th' );
    thElem.innerHTML = value;
    tableHead.appendChild( thElem );
  } );

  vals.forEach( value => {
    const tdElem = document.createElement( 'td' );
    tdElem.innerHTML = value;
    tableBody.appendChild( tdElem );
  } );
}

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
 * @param {number} housePrice - A home price.
 * @param {number} downPayment - A down payment amount.
 * @returns {number} Loan amount.
 */
function calcLoanAmount( housePrice, downPayment ) {
  const loan = unFormatUSD( housePrice ) - unFormatUSD( downPayment );

  if ( loan > 0 ) {
    return loan;
  }

  return 0;
}

/**
 * Calculate and render the loan amount in the format $100,000.
 * @param {HTMLNode} elem - HTML element to fill in with loan amount.
 * @param {number} loanAmount - A loan amount as a number.
 */
function renderLoanAmount( elem, loanAmount ) {
  elem.textContent = formatUSD( loanAmount, { decimalPlaces: 0 } );
}

module.exports = {
  calcLoanAmount,
  delay,
  formatTimestampMMddyyyy,
  renderAccessibleData,
  renderDatestamp,
  renderLoanAmount
};
