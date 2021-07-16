const encodeName = require( '../encode-name' );

const $ = document.querySelector.bind( document );

let value = '';

const displayValue = $( '.initials-value' );
const display = $( '.initials-display' );

function update(newValue) {
  value = newValue;
  if ( displayValue && display ) {
    if ( newValue ) {
      displayValue.textContent = newValue;
      display.style.display = '';
      display.setAttribute('aria-hidden', 'false');
    } else {
      display.style.display = 'none';
      display.setAttribute('aria-hidden', 'false');
    }
  }
}

function get() {
  return value;
}

function init() {
  // Show initials encoded in URL hash
  update(encodeName.decodeNameFromUrl( location.href ) || '');
}

export { init, get, update };
