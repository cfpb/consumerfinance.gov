import * as behavior from '../../../js/modules/util/behavior';

/**
 * Set up event handler for button to scroll to top of page.
 */
function init() {
  behavior.attach( 'submit-search', 'submit', event => {
    // event.preventDefault();
    console.log('submitted!');
  } );
}

window.addEventListener( 'load', () => {
  init();
} );
