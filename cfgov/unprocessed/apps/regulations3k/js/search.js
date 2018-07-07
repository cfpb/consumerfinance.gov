import * as behavior from '../../../js/modules/util/behavior';
import * as utils from './search-utils';
import { closest, queryOne as find } from '../../../js/modules/util/dom-traverse';

// Container that holds search results
const searchContainer = find( '#regs3k-results' );

function init() {
  // Override search form submission
  behavior.attach( 'submit-search', 'submit', handleSubmit );
  behavior.attach( 'submit-search', 'change', handleSubmit );
  // Attach search results handlers
  attachHandlers();
}

function attachHandlers() {
  behavior.attach( 'clear-filter', 'click', clearFilter );
  behavior.attach( 'clear-all', 'click', clearFilters );
}

function clearFilter( event ) {
  // Continue only if the X icon was clicked
  if ( event.target.tagName === 'BUTTON' ) {
    return;
  }
  const target = closest( event.target, 'button' );
  const checkbox = find( `#regulation-${ target.value }` );
  target.remove();
  checkbox.checked = false;
  handleSubmit( event );
}

function clearFilters( event ) {
  console.log('cleared all!');
}

function handleSubmit( event ) {
  event.preventDefault();
  const filters = document.querySelectorAll( 'input:checked' );
  const searchField = find( 'input[name=q]' );
  const searchTerms = utils.getSearchValues( searchField, filters );
  const baseUrl = window.location.href.split( '?' )[0];
  const searchParams = utils.serializeFormFields( searchTerms );
  const searchUrl = utils.buildSearchResultsURL( baseUrl, searchParams );
  utils.showLoading( searchContainer );
  utils.fetchSearchResults( searchUrl, ( err, data ) => {
    utils.hideLoading( searchContainer );
    if ( err ) {
      console.error( utils.handleError( 'search' ).msg );
    }
    searchContainer.innerHTML = data;
    // Reattach event handlers after tags are reloaded
    attachHandlers();
    return data;
  } );
}

window.addEventListener( 'load', () => {
  init();
} );
