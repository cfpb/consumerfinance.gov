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
    const searchTerms = utils.getSearchValues( search, filters );
    const baseUrl = window.location.href.split('?')[0];
    const searchParams = utils.serializeFormFields( searchTerms );
    const searchUrl = utils.buildSearchResultsURL( baseUrl, searchParams );
    utils.fetchSearchResults( searchUrl, ( err, data ) => {
      console.log( err );
      console.log( data );
    } );
  } );
}




window.addEventListener( 'load', () => {
  init();
} );
