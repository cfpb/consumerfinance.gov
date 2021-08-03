const encodeName = require( '../encode-name' );

const $ = document.querySelector.bind( document );

let value = '';

const displayValue = $( '.initials-value' );
const display = $( '.initials-display' );

/**
 * Update the initials in the page
 *
 * @param {string } newValue the new initials
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
 * Get the initials set
 *
 * @returns {string} The initials
 */
function get() {
  return value;
}

/**
 * Load the initials from the URL
 */
function init() {
  // Show initials encoded in URL hash
  update( encodeName.decodeNameFromUrl( location.href ) || '' );
}

export { init, get, update };
