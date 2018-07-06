import * as behavior from '../../../js/modules/util/behavior';

/**
 * Set up event handler to override search form submission.
 */
function init() {
  behavior.attach( 'submit-search', 'submit', event => {
    /* event.preventDefault();
       console.log('submitted!'); */
  } );
}

window.addEventListener( 'load', () => {
  init();
} );
