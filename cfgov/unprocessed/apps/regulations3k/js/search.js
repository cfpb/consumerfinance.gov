import * as behavior from '../../../js/modules/util/behavior';
import * as utils from './search-utils';
import { closest, queryOne as find } from '../../../js/modules/util/dom-traverse';

// Keep track of the most recent XHR request so that we can cancel it if need be
let searchRequest = {};

/**
 * Initialize search functionality.
 */
function init() {
  // Override search form submission
  behavior.attach( 'submit-search', 'submit', handleSubmit );
  behavior.attach( 'change-filter', 'change', handleFilter );
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
  // Continue only if the X icon was clicked and not the parent button
  let target = event.target.tagName.toLowerCase();
  if ( target !== 'svg' && target !== 'path' ) {
    return;
  }
  target = closest( event.target, '.a-tag' );
  const checkbox = find( `#regulation-${ target.dataset.value }` );
  // Remove the filter tag
  target.remove();
  // Uncheck the filter checkbox
  checkbox.checked = false;
  if ( event instanceof Event ) {
    handleFilter( event );
  }
}

/**
 * Remove all filters from the search results page.
 *
 * @param {Event} event Click event
 */
function clearFilters( event ) {
  const filterIcons = document.querySelectorAll( '.a-tag svg' );
  filterIcons.forEach( filterIcon => {
    const target = closest( filterIcon, 'button' );
    clearFilter( {
      target: filterIcon,
      value: target
    } );
  } );
  handleFilter( event );
}

/**
 * Handle keyword search form submission.
 *
 * @param {Event} event Click event
 * @returns {String} New page URL with search terms.
 */
function handleSubmit( event ) {
  if ( event instanceof Event ) {
    event.preventDefault();
  }
  const filters = document.querySelectorAll( 'input:checked' );
  const searchField = find( 'input[name=q]' );
  const searchTerms = utils.getSearchValues( searchField, filters );
  const baseUrl = window.location.href.split( '?' )[0];
  const searchParams = utils.serializeFormFields( searchTerms );
  const searchUrl = utils.buildSearchResultsURL( baseUrl, searchParams );
  window.location.assign( searchUrl );
  return searchUrl;
}

/**
 * Handle filter change events.
 *
 * @param {Event} event Click event
 */
function handleFilter( event ) {
  if ( event instanceof Event ) {
    event.preventDefault();
  }
  // Abort the previous search request if it's still active
  /* eslint no-empty: ["error", { "allowEmptyCatch": true }] */
  try {
    searchRequest.abort();
  } catch ( err ) { }
  const searchContainer = find( '#regs3k-results' );
  const filters = document.querySelectorAll( 'input:checked' );
  const searchField = find( 'input[name=q]' );
  const searchTerms = utils.getSearchValues( searchField, filters );
  const baseUrl = window.location.href.split( '?' )[0];
  const searchParams = utils.serializeFormFields( searchTerms );
  const searchUrl = utils.buildSearchResultsURL(
    baseUrl, searchParams, { partial: true }
  );
  // Update the filter query params in the URL
  utils.updateUrl( baseUrl, searchParams );
  utils.showLoading( searchContainer );
  searchRequest = utils.fetchSearchResults( searchUrl, ( err, data ) => {
    utils.hideLoading( searchContainer );
    if ( err !== null ) {
      // TODO: Add message banner above search results
      return console.error( utils.handleError( err ).msg );
    }
    searchContainer.innerHTML = data;
    // Update the query params in the URL
    utils.updateUrl( baseUrl, searchParams );
    // Reattach event handlers after tags are reloaded
    attachHandlers();
    return data;
  } );
}

// Provide the no-JS experience to browsers without `replaceState`
if ( 'replaceState' in window.history ) {
  window.addEventListener( 'load', () => {
    init();
  } );
} else {
  document.getElementById( 'main' ).className += ' no-js';
}
