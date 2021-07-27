const encodeName = require( '../encode-name' );

const $ = document.querySelector.bind( document );

let value = '';

const displayValue = $( '.initials-value' );
const display = $( '.initials-display' );

/**
 * Set initials in the page
 *
 * @param {string} newValue New initials
 */
function update( newValue ) {
  value = newValue;
  if ( displayValue && display ) {
    if ( newValue ) {
      displayValue.textContent = newValue;
      display.style.display = '';
      display.setAttribute( 'aria-hidden', 'false' );
    } else {
      display.style.display = 'none';
      display.setAttribute( 'aria-hidden', 'false' );
    }
  }
}

/**
 * Get user's initials
 *
 * @returns {string}
 */
function get() {
  return value;
}

/**
 * Update user's initials from URL
 */
function init() {
  // Show initials encoded in URL hash
  update( encodeName.decodeNameFromUrl( location.href ) || '' );
}

export { init, get, update };
