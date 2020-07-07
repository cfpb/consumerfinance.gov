const Analytics = require( './Analytics' );
const closest = require( './util/dom-traverse' ).closest;
const bindEvent = require( './util/dom-events' ).bindEvent;
const find = require( './util/dom-traverse' ).queryOne;

/* eslint-disable consistent-return */

/**
 * Sends the user interaction to Analytics
 * @param {string} action - The user's action
 * @param {string} label - The label associated with the action
 * @param {string} category - Optional category if it's not eRegs-related
 * @returns {object} Event data
 */
const sendEvent = ( action, label, category ) => {
  category = category || 'TDP Search Tool';
  const eventData = Analytics.getDataLayerOptions( action, label, category );
  Analytics.sendEvent( eventData );
  return eventData;
};

/**
 * getExpandable - Find the expandable the user clicked.
 *
 * @param {event} event Click event
 *
 * @returns {DOMNode|null} The expandable or null if it's not an expandable
 */
const getExpandable = event => {
  let el = closest( event.target, '.o-expandable_header' );
  el = el ? el : closest( event.target, '.o-expandable-facets_target' );
  el = el ? el : event.target;

  if (
    el.classList.contains( 'o-expandable_header' ) ||
    el.classList.contains( 'o-expandable-facets_target' )
  ) {
    return el;
  }
  return null;
};

/**
 * getExpandableState - Description
 *
 * @param {DOMNode} expandable Expandable's HTML element
 *
 * @returns {string} Expandable's state, either `open` or `close`
 */
const getExpandableState = expandable => {
  let state = 'collapse';
  if (
    expandable.classList.contains( 'o-expandable_target__expanded' ) ||
    expandable.classList.contains( 'is-open' )
  ) {
    state = 'expand';
  }
  return state;
};

/**
 * handleExpandableClick - Listen for clicks within a search page's content
 * and report to GA if they opened or closed an expandable.
 *
 * @param {event} event Click event
 * @param {method} sendEventMethod method
 * @returns {object} Event data
 */
const handleExpandableClick = ( event, sendEventMethod ) => {
  const expandable = getExpandable( event );
  if ( !expandable ) {
    return;
  }
  const action = `${ getExpandableState( expandable ) } filter`;
  let label = find( 'span.o-expandable_label', expandable );
  label = label ? label : find( 'span[aria-hidden=true]', expandable );
  if ( !label ) {
    return;
  }
  label = label.textContent.trim();

  if ( sendEventMethod ) {
    return sendEventMethod( action, label );
  }

  return sendEvent( action, label );
};

/**
 * handleFilterClick - Listen for filter clicks and report to GA.
 *
 * @param {event} event Click event
 * @param {method} sendEventMethod method
 * @returns {object} Event data
 */
const handleFilterClick = ( event, sendEventMethod ) => {
  const checkbox = event.target;
  if ( !checkbox.classList.contains( 'a-checkbox' ) ) {
    return;
  }
  const action = checkbox.checked ? 'filter' : 'remove filter';
  const label = checkbox.getAttribute( 'aria-label' );

  if ( sendEventMethod ) {
    return sendEventMethod( action, label );
  }

  return sendEvent( action, label );
};

/**
 * handleClearFilterClick - Listen for clear filter clicks and report to GA.
 *
 * @param {event} event Click event
 * @param {method} sendEventMethod method
 * @returns {object} Event data
 */
const handleClearFilterClick = ( event, sendEventMethod ) => {
  // Continue only if the X icon was clicked and not the parent button
  let target = event.target.tagName.toLowerCase();
  if ( target !== 'svg' && target !== 'path' ) {
    return;
  }
  target = closest( event.target, '.a-tag[data-js-hook=behavior_clear-filter]' );

  if ( !target ) {
    return;
  }
  const action = 'remove filter';
  const label = target.textContent.trim();

  if ( sendEventMethod ) {
    return sendEventMethod( action, label );
  }

  return sendEvent( action, label );
};

/**
 * getPaginator - Find the paginator the user clicked.
 *
 * @param {event} event Click event
 *
 * @returns {DOMNode|null} The checkbox div or null if it's not a checkbox
 */
const getPaginator = event => {
  const el = closest( event.target, '.a-btn' ) || event.target;
  if ( el.classList.contains( 'a-btn' ) ) {
    return el;
  }
  return null;
};

/**
 * handlePaginationClick - Listen for pagination clicks and report to GA.
 *
 * @param {event} event Click event
 * @param {method} sendEventMethod method
 * @returns {object} Event data
 */
const handlePaginationClick = ( event, sendEventMethod ) => {
  const paginator = getPaginator( event );
  if ( !paginator ) {
    return;
  }

  const isNextButton = paginator.classList.contains( 'm-pagination_btn-next' );
  const isPrevButton = paginator.classList.contains( 'm-pagination_btn-prev' );
  const isDisabled = paginator.classList.contains( 'a-btn__disabled' );

  if (
    !paginator.href ||
    isDisabled ||
     !isNextButton && !isPrevButton
  ) {
    return;
  }

  const action = isNextButton ? 'next page' : 'previous page';
  let label = paginator.href.match( /\?.*page=(\d+)/ );
  if ( !label ) {
    return;
  }
  label = isNextButton ? parseInt( label[1], 10 ) - 1 : parseInt( label[1], 10 ) + 1;


  if ( sendEventMethod ) {
    return sendEventMethod( action, label );
  }

  return sendEvent( action, label );
};

/**
 * getClearBtn - Find the clear all filters button.
 *
 * @param {event} event Click event
 *
 * @returns {DOMNode|null} The checkbox div or null if it's not a checkbox
 */
const getClearBtn = event => {
  const el = closest( event.target, '.results_filters-clear' ) || event.target;
  if ( el.classList.contains( 'results_filters-clear' ) ) {
    return el;
  }
  return null;
};

/**
 * handleClearAllClick - Listen for clear all filters clicks and report to GA.
 *
 * @param {event} event Click event
 * @param {method} sendEventMethod method
 * @returns {object} Event data
 */
const handleClearAllClick = ( event, sendEventMethod ) => {
  const clearBtn = getClearBtn( event );
  if ( !clearBtn ) {
    return;
  }
  const tagsWrapper = clearBtn.parentElement;
  const tags = tagsWrapper.querySelectorAll( '.a-tag' );
  if ( !tags || tags.length === 0 ) {
    return;
  }
  const tagNames = [];
  for ( let i = 0; i < tags.length; i++ ) {
    if ( tagsWrapper.contains( tags[i] ) ) {
      tagNames.push( tags[i].textContent.trim() );
    }
  }
  if ( tagNames.length === 0 ) {
    return;
  }
  const action = 'clear all filters';
  const label = tagNames.join( '|' );

  if ( sendEventMethod ) {
    return sendEventMethod( action, label );
  }

  return sendEvent( action, label );
};

/**
 * handleFetchSearchResults - Listen for AJAX fetchSearchResults and report to GA.
 *
 * @param {string} searchTerm string
 * @param {method} sendEventMethod method
 * @returns {object} Event data
 */
const handleFetchSearchResults = ( searchTerm, sendEventMethod ) => {

  if ( searchTerm.length === 0 ) {
    return;
  }

  // Send the keywords that return 0 results to Analytics.
  const resultsCountBlock = find( '#tdp-search-facets-and-results .results_count' );
  if ( resultsCountBlock ) {
    const resultsCount = resultsCountBlock.getAttribute( 'data-results-count' );

    // Check if result count is 0
    if ( resultsCount === '0' ) {
      const action = 'noSearchResults';
      const label = searchTerm.toLowerCase() + ':0';

      if ( sendEventMethod ) {
        sendEventMethod( action, label );
      } else {
        sendEvent( action, label );
      }
    }
  }

  // Send the keyword to Analytics.
  const action = 'search';
  const label = searchTerm.toLowerCase();
  if ( sendEventMethod ) {
    return sendEventMethod( action, label );
  }
  return sendEvent( action, label );
};

/**
 * bindAnalytics - Set up analytics reporting.
 *
 * @param {method} sendEventMethod method
 */
const bindAnalytics = sendEventMethod => {
  const searchContent = find( '#tdp-search-facets-and-results' );
  if ( searchContent ) {
    bindEvent( searchContent, {
      click: event => handleExpandableClick( event, sendEventMethod )
    } );

    bindEvent( searchContent, {
      click: event => handleFilterClick( event, sendEventMethod )
    } );

    bindEvent( searchContent, {
      click: event => handleClearFilterClick( event, sendEventMethod )
    } );

    bindEvent( searchContent, {
      click: event => handlePaginationClick( event, sendEventMethod )
    } );
  }
};

module.exports = {
  getExpandable,
  getPaginator,
  getClearBtn,
  getExpandableState,
  handleExpandableClick,
  handleFilterClick,
  handleClearFilterClick,
  handlePaginationClick,
  handleClearAllClick,
  handleFetchSearchResults,
  sendEvent,
  bindAnalytics
};
