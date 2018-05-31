import {
  Delay,
  track
} from './util/analytics-util';

/* Search for support of the matches() method by looking at
   browser prefixes.
   @param {HTMLNode} elem
   The element to check for support of matches() method.
   @returns {Function} The appropriate matches() method of elem. */
function _getMatchesMethod( elem ) {
  return elem.matches ||
         elem.webkitMatchesSelector ||
         elem.mozMatchesSelector ||
         elem.msMatchesSelector;
}

/* Get the nearest parent node of an element.
   @param {HTMLNode} elem - A DOM element.
   @param {string} selector - CSS selector.
   @returns {HTMLNode} Nearest parent node that matches the selector. */
function closest( elem, selector ) {
  elem = elem.parentNode;

  const matchesSelector = _getMatchesMethod( elem );
  let match;

  while ( elem ) {
    if ( matchesSelector.bind( elem )( selector ) ) {
      match = elem;
    } else {
      elem = elem.parentElement;
    }

    if ( match ) { return elem; }
  }

  return null;
}

// HMDA Explore custom analytics file

const HMDAAnalytics = ( function() {

  // Collapsible open and close
  const divFilterEls = document.querySelectorAll( '#all div.filter' );
  for ( let i = 0, len = divFilterEls.length; i < len; i++ ) {
    divFilterEls[i].addEventListener( 'click', _handleDivFilterClick );
  }

  /**
   * Handle clicks on filter divs.
   * @param       {MouseEvent} evt - Event object.
   */
  function _handleDivFilterClick( evt ) {
    const target = evt.target;
    let action = 'Filter Expandable Opened';
    if ( target.classList.contains( 'closed' ) ) {
      action = 'Filter Expandable Closed';
    }
    const label = target.getAttribute( 'id' );
    track( 'HMDA Explore Interactions', action, label );
  }

  // Chosen menu selections for Summary Table Variables
  const selectChznSingleEls = document.querySelectorAll( 'select.chzn-single' );
  for ( let j = 0, len = selectChznSingleEls.length; j < len; j++ ) {
    selectChznSingleEls[j].addEventListener( 'change', _handleSelectChange );
  }

  /**
   * Handle select menu changes.
   * @param {Event} evt - Event object.
   */
  function _handleSelectChange( evt ) {
    const target = evt.target;
    const label = target.parentNode.querySelector( '.chzn-container a.chzn-single' ).textContent;
    const parent = closest( target, 'div' );
    const divs = document.querySelectorAll( '.drop-downs > div' );
    const n = divs.indexOf( parent ) + 1;
    const action = 'Variable Dropdown Menu #' + n;
    track( 'HMDA Explore Interactions', action, label );
  };

  // Chosen menu selections for Year filter
  const selectAsOfYearDelay = new Delay();
  const selectAsOfYear = document.querySelector( 'select#as_of_year' );
  selectAsOfYear.addEventListener( 'change', function( evt ) {
    const lastItem = document.querySelector( '#as_of_year_chzn .search-choice:last' );
    const label = lastItem.textContent;
    selectAsOfYearDelay( () => {
      track( 'HMDA Explore Interactions', 'Year Dropdown', label );
    }, 250 );
  } );

  // Chosen menu selections for suggested filters
  const selectSuggestedEl = document.querySelector( 'select#suggested' );
  selectSuggestedEl.addEventListener( 'change', function( evt ) {
    const target = evt.target;
    const label = target.value;
    track( 'HMDA Explore Interactions', 'Suggested Dropdown', label );
  } );

} )();
