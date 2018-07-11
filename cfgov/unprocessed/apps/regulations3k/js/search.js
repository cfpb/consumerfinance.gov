import * as behavior from '../../../js/modules/util/behavior';
import * as utils from './search-utils';
import { closest, queryOne as find } from '../../../js/modules/util/dom-traverse';

/**
 * Initialize search functionality.
 */
function init() {
  // Override search form submission
  behavior.attach( 'submit-search', 'submit', handleSubmit );
  behavior.attach( 'submit-search', 'change', handleSubmit );
  attachHandlers();
}

/**
 * Attach search results handlers
 */
function attachHandlers() {
  behavior.attach( 'clear-filter', 'click', clearFilter );
  behavior.attach( 'clear-all', 'click', clearFilters );
}

/**
 * Remove a filter from the search results page.
 *
 * @param {Event} event Click event
 */
function clearFilter( event ) {
  // Continue only if the X icon was clicked
  if ( event.target.tagName === 'BUTTON' ) {
    return;
  }
  const target = closest( event.target, 'button' );
  const checkbox = find( `#regulation-${ target.value }` );
  // Remove the filter tag
  target.remove();
  // Uncheck the filter checkbox
  checkbox.checked = false;
  handleSubmit( event );
}

/**
 * Remove all filters from the search results page.
 *
 * @param {Event} event Click event
 */
function clearFilters( event ) {
  // TODO: Implement this.
  console.log( 'cleared all!' );
}

/**
 * Remove all filters from the search results page.
 *
 * @param {Event} event Click event
 */
function handleSubmit( event ) {
  event.preventDefault();
  const searchContainer = find( '#regs3k-results' );
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
      // TODO: Add message banner above search results
      return console.error( utils.handleError( 'no-results' ).msg );
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
