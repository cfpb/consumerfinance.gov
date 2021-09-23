import Analytics from '../../../js/modules/Analytics';
import { closest, queryOne } from '@cfpb/cfpb-atomic-component/src/utilities/dom-traverse.js';

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
 * Sends the user survey interaction to Analytics
 * @param {string} action - The user's action
 * @param {string} label - The label associated with the action
 * @returns {object} Event data
 */
const sendSurveyEvent = ( action, label) => {
  const category = 'Student Survey Interaction';
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
  let label = queryOne( 'span.o-expandable_label', expandable );
  label = label ? label : queryOne( 'span[aria-hidden=true]', expandable );
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
  const resultsCountBlock = queryOne( '#tdp-search-facets-and-results .results_count' );
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
 * handleSurveySwitchGradeClick - Listen for Switch grades click and report to GA.
 *
 * @param {event} event Click event
 * @param {method} sendEventMethod method
 * @returns {object} Event data
 */
const handleSurveySwitchGradeClick = ( event, sendEventMethod ) => {
  const link = closest( event.target, '.a-link__jump' ) || event.target;
  if ( !link.classList.contains( 'a-link__jump' ) ) {
    return;
  }
  const action = link.textContent.trim();
  const grade_level = link.getAttribute('data-tdp_grade_level');
  const label = 'Switch grades from ' + grade_level;
  if ( sendEventMethod ) {
    return sendEventMethod( action, label );
  }

  return sendSurveyEvent( action, label );
};

/**
 * handleSurveyPrivacyModalClick - Listen for Privacy statement click and report to GA.
 *
 * @param {event} event Click event
 * @param {method} sendEventMethod method
 * @returns {object} Event data
 */
const handleSurveyPrivacyModalClick = ( event, sendEventMethod ) => {
  const link = closest( event.target, '[data-open-modal="modal-privacy"]' ) || event.target;
  if ( link.getAttribute( 'data-open-modal' ) != 'modal-privacy' ) {
    return;
  }
  const action = link.textContent.trim();
  const grade_level = link.getAttribute('data-tdp_grade_level');
  const label = grade_level + ": " + question;
  if ( sendEventMethod ) {
    return sendEventMethod( action, label );
  }

  return sendSurveyEvent( action, label );
};

/**
 * handleSurveyLetsDoThisClick - Listen for Let's do this click and report to GA.
 *
 * @param {event} event Click event
 * @param {method} sendEventMethod method
 * @returns {object} Event data
 */
const handleSurveyLetsDoThisClick = ( event, sendEventMethod ) => {
  const link = closest( event.target, 'a.survey-entry-link' ) || event.target;
  if ( !link.classList.contains( 'survey-entry-link' ) ) {
    return;
  }
  const action = link.textContent.trim();
  const grade_level = link.getAttribute('data-tdp_grade_level');
  const label = grade_level;
  if ( sendEventMethod ) {
    return sendEventMethod( action, label );
  }

  return sendSurveyEvent( action, label );
};

/**
 * handleSurveyChoiceChange - Listen for radio button value change and report to GA.
 *
 * @param {event} event Click event
 * @param {method} sendEventMethod method
 * @returns {object} Event data
 */
const handleSurveyChoiceChange = ( event, sendEventMethod ) => {
  const radio = closest( event.target, 'input.tdp-survey__choice-question' ) || event.target;
  if ( !radio.classList.contains( 'tdp-survey__choice-question' ) || !radio.checked ) {
    return;
  }
  const action = 'Radio Button Clicked';
  const wrapper = closest( radio, 'div.wrapper.tdp-survey');
  const grade_level = wrapper.getAttribute('data-tdp_grade_level');
  const parent_fieldset = closest( radio, 'fieldset' );
  const question = queryOne( 'legend.tdp-question-legend', parent_fieldset );
  const answer = queryOne( 'label', radio.parentElement);
  const label = grade_level + ': ' + question.textContent.trim() + ' (' + answer.textContent.trim() + ')';
  if ( sendEventMethod ) {
    return sendEventMethod( action, label );
  }

  return sendSurveyEvent( action, label );
};

/**
 * handleSurveyErrorNoticeClick - Listen for error notification click and report to GA.
 *
 * @param {event} event Click event
 * @param {method} sendEventMethod method
 * @returns {object} Event data
 */
const handleSurveyErrorNoticeClick = ( event, sendEventMethod ) => {
  const link = closest( event.target, '.m-notification__error a' ) || event.target;
  if ( link.getAttribute( 'href' )  != '#' ) {
    return;
  }
  const action = 'Anchor: Missed Question';
  const wrapper = closest( link, 'div.wrapper.tdp-survey');
  const grade_level = wrapper.getAttribute( 'data-tdp_grade_level' );
  const section = +queryOne( 'div[data-page-idx]', wrapper).getAttribute( 'data-page-idx' ) + 1;
  const question = link.textContent.trim();
  const label = grade_level + ': Section ' + section + ' | ' + question;
  if ( sendEventMethod ) {
    return sendEventMethod( action, label );
  }

  return sendSurveyEvent( action, label );
};

/**
 * bindAnalytics - Set up analytics reporting.
 *
 * @param {method} sendEventMethod method
 */
const bindAnalytics = sendEventMethod => {
  const searchContent = queryOne( '#tdp-search-facets-and-results' );
  if ( searchContent ) {
    searchContent.addEventListener( 'click', event => {
      handleExpandableClick( event, sendEventMethod );
      handleFilterClick( event, sendEventMethod );
      handleClearFilterClick( event, sendEventMethod );
      handlePaginationClick( event, sendEventMethod );
    } );
  }
  // Survey section event listeners.
  const surveyContent = queryOne( '.tdp-survey' );
  if ( surveyContent ) {
    surveyContent.addEventListener( 'click', event => {
      handleSurveySwitchGradeClick( event, sendEventMethod );
      handleSurveyPrivacyModalClick( event, sendEventMethod );
      handleSurveyLetsDoThisClick( event, sendEventMethod );
      handleSurveyErrorNoticeClick( event, sendEventMethod );
    } );

    surveyContent.addEventListener( 'change', event => {
      handleSurveyChoiceChange( event, sendEventMethod);
    } );
  }
};

export {
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
  handleSurveySwitchGradeClick,
  handleSurveyPrivacyModalClick,
  handleSurveyLetsDoThisClick,
  handleSurveyChoiceChange,
  handleSurveyErrorNoticeClick,
  sendEvent,
  sendSurveyEvent,
  bindAnalytics
};
