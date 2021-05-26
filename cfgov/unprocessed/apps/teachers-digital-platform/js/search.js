const behavior = require( '../../../js/modules/util/behavior' );
const utils = require( './search-utils' );
import { closest, queryOne as find } from '@cfpb/cfpb-atomic-component/src/utilities/dom-traverse.js';
import expandableFacets from './expandable-facets';
import cfExpandables from '@cfpb/cfpb-expandables/src/Expandable';
const analytics = require( './tdp-analytics' );
const fetch = require( './utils' ).fetch;
const ClearableInput = require( './ClearableInput' ).ClearableInput;

// Keep track of the most recent XHR request so that we can cancel it if need be
let searchRequest = {};

/**
 * Initialize search functionality.
 */
function init() {
  if ( 'replaceState' in window.history ) {
    // Override search form submission
    attachHandlers();
  } else {
    // This case already handled inline at the bottom
  }
}

/**
 * Attach search results handlers
 */
function attachHandlers() {
  addDataGtmIgnore();
  behavior.attach( 'submit-search', 'submit', handleSubmit );
  behavior.attach( 'change-filter', 'change', handleFilter );
  behavior.attach( 'clear-filter', 'click', clearFilter );
  behavior.attach( 'clear-all', 'click', clearFilters );
  behavior.attach( 'clear-search', 'clear', clearSearch );
  cfExpandables.init();
  expandableFacets.init();
  const inputContainsLabel = document.querySelector( '.tdp-activity-search .input-contains-label' );
  if ( inputContainsLabel ) {
    const clearableInput = new ClearableInput( inputContainsLabel );
    clearableInput.init();
  }
}

/**
 * Ignore analytics for previous and next pagination buttons
 */
function addDataGtmIgnore() {
  const ignoreBtns = [
    'a.m-pagination_btn-next',
    'a.m-pagination_btn-prev'
  ];

  for ( let i = 0; i < ignoreBtns.length; i++ ) {
    const btn = document.querySelector( ignoreBtns[i] );
    if ( btn ) {
      btn.setAttribute( 'data-gtm_ignore', 'true' );
    }
  }
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
  const checkbox = find( `${ target.getAttribute( 'data-value' ) }` );
  // Remove the filter tag
  removeTag( target );
  // Uncheck the filter checkbox
  checkbox.checked = false;
  if ( event instanceof Event ) {
    handleFilter( event, checkbox );
  }
}

/**
 * Remove a filter tag from the search results page.
 * node.remove() isn't supported by IE so we have to removeChild();
 *
 * @param {Node} tag Filter tag HTML element
 */
function removeTag( tag ) {
  if ( tag.parentNode !== null ) {
    tag.parentNode.removeChild( tag );
  }
}


/**
 * Remove all filters from the search results page.
 *
 * @param {Event} event Click event
 */
function clearFilters( event ) {
  // Handle Analytics here before tags vanish.
  analytics.handleClearAllClick( event );

  let filterIcons = document.querySelectorAll( '.a-tag svg' );
  // IE doesn't support forEach w/ node lists so convert it to an array.
  filterIcons = Array.prototype.slice.call( filterIcons );
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
 * Trigger a form submit after Clear Search is clicked.
 *
 * @param {Event} event Click event
 */
function clearSearch( event ) {
  if ( event instanceof Event ) {
    event.preventDefault();
  }
  handleSubmit( event );
}

/**
 * Handle keyword search form submission.
 *
 * @param {Event} event Click event
 * @returns {String} New page URL with search terms
 */
function handleSubmit( event ) {
  if ( event instanceof Event ) {
    event.preventDefault();
  }
  // fetch search results without applying filters when searching
  const searchUrl = fetchSearchResults();
  return searchUrl;
}

/**
 * fetch search results based on filters and keywords.
 *
 * @param {NodeList} filters List of filter checkboxes
 * @returns {String} New page URL with search terms
 */
function fetchSearchResults( filters = [] ) {
  const searchContainer = find( '#tdp-search-facets-and-results' );
  const baseUrl = window.location.href.split( '?' )[0];
  const searchField = find( 'input[name=q]' );
  const searchTerms = utils.getSearchValues( searchField, filters );
  const searchParams = utils.serializeFormFields( searchTerms );

  const searchUrl = utils.buildSearchResultsURL(
    baseUrl, searchParams, { partial: true }
  );
  utils.updateUrl( baseUrl, searchParams );
  utils.showLoading( searchContainer );
  searchRequest = fetch( searchUrl, ( err, data ) => {
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
    // Send search query to Analytics.
    analytics.handleFetchSearchResults( searchField.value );
    return data;
  } );
  return searchUrl;
}

/**
 * Handle filter change events.
 *
 * @param {Event} event Click event
 * @param {DOMElement} target DOM element
 * @returns {String} New page URL with search terms
 */
function handleFilter( event, target = null ) {
  if ( event instanceof Event ) {
    event.preventDefault();
  }
  // Abort the previous search request if it's still active
  /* eslint no-empty: ["error", { "allowEmptyCatch": true }] */
  try {
    searchRequest.abort();
  } catch ( err ) { }
  target = target ? target : event.target;
  const wrapperLI = target.parentElement.parentElement;
  if ( wrapperLI && wrapperLI.tagName.toLowerCase() === 'li' ) {

    // Check all children if parent is checked.
    const checkboxes = wrapperLI.querySelectorAll(
      'ul>li input[type=checkbox]'
    );
    for ( let i = 0; i < checkboxes.length; i++ ) {
      if ( wrapperLI.contains( checkboxes[i] ) === true && checkboxes[i] !== target ) {
        checkboxes[i].checked = target.checked;
      }
    }
    // If this is a child checkbox, update the parent checkbox.
    const parentLI = wrapperLI.parentElement.parentElement;
    const parentUL = wrapperLI.parentElement.parentElement.parentElement;
    if ( parentUL && parentUL.tagName.toLowerCase() === 'ul' ) {
      const parentCheckbox = parentLI.querySelector(
        'div>input[type=checkbox]'
      );
      if ( parentCheckbox && parentCheckbox.parentElement.parentElement === parentLI ) {
        _updateParentFilter( parentCheckbox );
      }
    }
  }

  const filters = document.querySelectorAll( 'input:checked' );
  const searchUrl = fetchSearchResults( filters );
  return searchUrl;
}

/**
 * Traverse parents and update their checkbox values.
 *
 * @param {DOMElement} element DOM element
 */
function _updateParentFilter( element ) {
  const wrapper = element.parentElement.parentElement;
  const checkboxes = wrapper.querySelectorAll(
    'ul>li input[type=checkbox]'
  );

  const children = [];
  const checkedChildren = [];
  for ( let i = 0; i < checkboxes.length; i++ ) {
    if ( wrapper.contains( checkboxes[i] ) === true ) {
      children.push( checkboxes[i] );
      if ( checkboxes[i].checked === true ) {
        checkedChildren.push( checkboxes[i] );
      }
    }
  }

  if ( children ) {
    if ( children.length !== checkedChildren.length ) {
      element.checked = false;
    }
  }
  // Loop through ancestors and make sure they are checked or unchecked
  const parentWrapper = wrapper.parentElement.parentElement;
  const parentCheckbox = parentWrapper.querySelector(
    'div>input[type=checkbox]'
  );
  if ( parentCheckbox && parentCheckbox.parentElement === parentWrapper ) {
    _updateParentFilter( parentCheckbox );
  }
}

// Provide the no-JS experience to browsers without `replaceState`
if ( 'replaceState' in window.history ) {
  // This case handled in init() above
} else {
  document.getElementById( 'main' ).className += ' no-js';
}

export { init };
