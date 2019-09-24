import {
  Delay,
  track
} from './util/analytics-util';

// HMDA Explore custom analytics file

const HMDAAnalytics = ( function() {

  // Collapsible open and close
  const divFilterEls = document.querySelectorAll( '#all div.filter' );
  for ( let i = 0, len = divFilterEls.length; i < len; i++ ) {
    divFilterEls[i].addEventListener( 'click', _handleDivFilterClick );
  }

  /**
   * Handle clicks on filter divs.
   * @param {MouseEvent} evt - Event object.
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
  const selectChznSingleEls = document.querySelectorAll( 'select.chzn-single + .chzn-container' );
  for ( let j = 0, len = selectChznSingleEls.length; j < len; j++ ) {
    selectChznSingleEls[j].addEventListener( 'mouseup', _handleSelectChange );
  }

  /**
   * Handle select menu changes.
   * @param {Event} evt - Event object.
   */
  function _handleSelectChange( evt ) {
    const target = evt.currentTarget;

    // If the drop-down isn't closed, we're still selecting an item.
    if ( target.classList.contains( 'chzn-with-drop' ) ) {
      return;
    }

    const label = target.querySelector( 'a.chzn-single' ).textContent;

    // Find the number of this drop-down.
    const id = target.id;
    let n;
    if ( id === 'calculate_by_chzn' ) {
      n = 4;
    } else {
      // This relies on the div's id in format variable[n]_chzn.
      n = Number( target.id.substr( -6, 1 ) ) + 1;
    }

    const action = 'Variable Dropdown Menu #' + n;
    track( 'HMDA Explore Interactions', action, label );
  }

  // Chosen menu selections for Year filter
  const selectAsOfYearDelay = new Delay();
  const selectAsOfYear = document.querySelector( 'div#as_of_year_chzn' );
  selectAsOfYear.addEventListener( 'mouseup', function( evt ) {
    const target = evt.currentTarget;
    const nodes = target.querySelectorAll( '.search-choice' );

    // If the drop-down isn't closed, we're still selecting an item.
    if ( target.classList.contains( 'chzn-with-drop' ) ||
         nodes.length === 0 ) {
      return;
    }

    const lastItem = nodes[nodes.length - 1];
    const label = lastItem.textContent;
    selectAsOfYearDelay( () => {
      track( 'HMDA Explore Interactions', 'Year Dropdown', label );
    }, 250 );
  } );

  // Chosen menu selections for suggested filters
  const selectSuggestedEl = document.querySelector( '#suggested_chzn' );
  selectSuggestedEl.addEventListener( 'mouseup', function( evt ) {
    const target = evt.currentTarget;

    // If the drop-down isn't closed, we're still selecting an item.
    if ( target.classList.contains( 'chzn-with-drop' ) ) {
      return;
    }

    const label = target.querySelector( 'a.chzn-single' ).textContent;
    track( 'HMDA Explore Interactions', 'Suggested Dropdown', label );
  } );

} )();
