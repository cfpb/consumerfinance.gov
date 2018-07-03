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
  const searchField = find( '[name=q]' );
  const searchTerms = utils.getSearchValues( searchField, filters );
  const baseUrl = window.location.href.split( '?' )[0];
  const searchParams = utils.serializeFormFields( searchTerms );
  const searchUrl = utils.buildSearchResultsURL( baseUrl, searchParams );
  showLoading();
  utils.fetchSearchResults( searchUrl, ( err, data ) => {
    hideLoading();
    if ( err ) {
      return handleError( 'search' );
    }
    searchContainer.innerHTML = data;
    // Reattach event handlers after tags are reloaded
    attachHandlers();
    return data;
  } );
}

function showLoading( ) {
  searchContainer.style.opacity = .3;
}

function hideLoading( ) {
  searchContainer.style.opacity = 1;
}

function handleError( err ) {
  switch ( err ) {
    case 'no-results':
      console.log('Your query returned zero results.');
      break;
    case 'search':
      console.log('Sorry, our search engine is temporarily down.');
      break;
    default:
      console.log('Sorry, an error occurred.');
      break;
  }
}

window.addEventListener( 'load', () => {
  init();
} );
