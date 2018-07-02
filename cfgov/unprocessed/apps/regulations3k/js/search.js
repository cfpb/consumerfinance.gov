import * as behavior from '../../../js/modules/util/behavior';
import * as utils from './search-utils';

/**
 * Set up event handler to override search form submission.
 */
function init() {
  behavior.attach( 'submit-search', 'submit', event => {
    event.preventDefault();
    const filters = document.querySelectorAll( 'input:checked' );
    const search = document.querySelector('[name=q]');
    console.log( utils.getSearchValues( search, filters ) );
  } );
}




window.addEventListener( 'load', () => {
  init();
} );
