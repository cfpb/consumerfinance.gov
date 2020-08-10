import DT from './dom-tools';

let count = 1;

/**
 * Reset the address inputs to be only one input like when the page loaded.
 */
function reset() {
  count = 1;

  DT.applyAll( '.input-address', function( element, index ) {

    if ( element.getAttribute( 'name' ) === 'address1' ) {
      element.value = '';
      DT.removeClass( element, 'error' );
    } else {
      DT.removeEl( element );
    }
  } );

  DT.removeClass( '#add-another', 'u-hidden' );
}

/**
 * Add a new address input (up to 10).
 */
function add() {
  count++;
  if ( count === 10 ) {
    DT.addClass( '#add-another', 'u-hidden' );
  }

  const previous = count - 1;

  if ( DT.getEl( '#address' + previous ).value === '' ) {
    DT.addClass( '#address' + previous, 'error' );
  } else {
    DT.removeClass( '#address' + previous, 'error' );
  }

  const addressElementContainer = DT.getEl( '#address1' ).cloneNode( true );
  addressElementContainer.setAttribute( 'id', 'address' + count );
  const addressElement = addressElementContainer.querySelector( 'input' );
  addressElement.setAttribute( 'name', 'address' + count );
  addressElement.value = '';
  DT.addEl( '.input-container', addressElementContainer );
  addressElement.focus();
}

/**
 * Add an error class to an address input if it is empty.
 * @param {Object} evt - A blur event object.
 */
function toggleError( evt ) {
  const target = evt.target;
  if ( evt.target.value === '' ) {
    DT.addClass( target, 'error' );
  } else {
    DT.removeClass( target, 'error' );
  }
}


export default {
  reset,
  add,
  toggleError
};
