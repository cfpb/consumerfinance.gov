import formatDate from 'date-format';
import formatUSD from 'format-usd';
import unFormatUSD from 'unformat-usd';

/**
 * Check if the house price entered is 0
 * @param {string|number} price - A price.
 * @returns {boolean} True if price is zero, false otherwise.
 */
function checkIfZero( price ) {
  if ( price === '0' || +Number( price ) === 0 ) {
    return true;
  }
  return false;
}

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
 * @param  {number} keyCode - A key code.
 * @returns {boolean} True if key is forbidden, false otherwise.
 */
function isKeyAllowed( keyCode ) {
  /* `FORBIDDEN_KEYS` are as follows:
  9 = tab
  37, 38, 39, 40 = arrow keys.
  13 = enter
  16 = shift */
  const FORBIDDEN_KEYS = [ 9, 37, 38, 39, 40, 13, 16 ];

  if ( FORBIDDEN_KEYS.indexOf( keyCode ) !== -1 ) {
    return false;
  }
  return true;
}

/**
 * @param  {HTMLNode} elem - An HTML element to check for u-hidden class.
 * @returns {boolean} True is the element is visible, false otherwise.
 */
function isVisible( elem ) {
  return !elem.classList.contains( 'u-hidden' );
}

/**
 * Add commas to numbers where appropriate.
 * @param {string} value - Old value where commas will be added.
 * @returns {string} Value with commas and no dollar sign.
 */
function removeDollarAddCommas( value ) {
  let parseValue = unFormatUSD( value );
  parseValue = formatUSD( { amount: parseValue, decimalPlaces: 0 } ).replace( '$', '' );
  return parseValue;
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
  let formattedTime;
  if ( time ) {
    formattedTime = formatTimestampMMddyyyy( time );
  }

  elem.textContent = formattedTime;
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
  elem.textContent = formatUSD( { amount: loanAmount, decimalPlaces: 0 } );
}


/**
 * Set value(s) of all HTML elements in the control panel.
 * @param {string} fields - TODO: Add description.
 */
function setSelections( fields ) {
  let val;
  let key;
  for ( key in fields ) {
    if ( Object.prototype.hasOwnProperty.call( fields, key ) ) {
      val = fields[key];
      const el = document.querySelector( '#' + key );
      if ( el ) {
        setSelection( el, val );
      }
    }
  }
}

/**
 * Set value(s) of an individual HTML element in the control panel.
 * @param  {HTMLNode} el An HTML input element on the page.
 * @param  {string} val Value to set inside the HTML element.
 */
function setSelection( el, val ) {

  const placeHolders = document.querySelectorAll( '[placeholder]' );
  let isInPlaceholders = false;
  for ( let i = 0, len = placeHolders.length; i < len; i++ ) {
    if ( placeHolders[i] === el ) {
      isInPlaceholders = true;
      break;
    }
  }
  if ( isInPlaceholders ) {
    el.setAttribute( 'placeholder', val );
  } else {
    el.value = val;
  }
}

export {
  calcLoanAmount,
  checkIfZero,
  delay,
  formatTimestampMMddyyyy,
  isKeyAllowed,
  isVisible,
  removeDollarAddCommas,
  renderAccessibleData,
  renderDatestamp,
  renderLoanAmount,
  setSelections
};
