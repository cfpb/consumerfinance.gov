const { INITIALS_LIMIT } = require( './config' );
const encodeName = require( '../encode-name' );

const $ = document.querySelector.bind( document );

let value = '';

/**
 * Update the initials in the page
 *
 * @param {string } newValue the new initials
 */
function update( newValue ) {
  const displayValue = $( '.initials-value' );
  const display = $( '.initials-display' );

  value = newValue;
  if ( displayValue && display ) {
    if ( newValue ) {
      displayValue.textContent = newValue;
      display.style.display = '';
      display.setAttribute( 'aria-hidden', 'false' );
    } else {
      display.style.display = 'none';
      display.setAttribute( 'aria-hidden', 'true' );
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
  let fromUrl = encodeName.decodeNameFromUrl( location.href ) || '';
  if ( fromUrl.length > INITIALS_LIMIT ) {
    // Definitely invalid, reject.
    fromUrl = '';
  }

  update( fromUrl );
}

export { encodeName, init, get, update };
