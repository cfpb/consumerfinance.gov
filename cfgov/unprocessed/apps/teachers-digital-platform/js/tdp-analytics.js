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
const sendSurveyEvent = ( action, label ) => {
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
        /* istanbul ignore next */
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

  /* istanbul ignore next */
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
  const grade_level = link.getAttribute( 'data-tdp_grade_level' );
  const label = 'Switch grades from ' + grade_level;
  if ( sendEventMethod ) {
    return sendEventMethod( action, label );
  }

  /* istanbul ignore next */
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
  if ( link.getAttribute( 'data-open-modal' ) !== 'modal-privacy' ) {
    return;
  }
  const action = link.textContent.trim();
  const grade_level = link.getAttribute( 'data-tdp_grade_level' );
  const label = grade_level;
  if ( sendEventMethod ) {
    return sendEventMethod( action, label );
  }

  /* istanbul ignore next */
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
  const grade_level = link.getAttribute( 'data-tdp_grade_level' );
  const label = grade_level;
  if ( sendEventMethod ) {
    return sendEventMethod( action, label );
  }

  /* istanbul ignore next */
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
  const radio = closest( event.target, 'input.tdp-survey__choice-question' );
  if ( !radio || !radio.checked ) {
    return;
  }
  const action = 'Radio Button Clicked';
  const wrapper = closest( radio, 'div.wrapper.tdp-survey' );
  const grade_level = wrapper.getAttribute( 'data-tdp_grade_level' );
  const parent_fieldset = closest( radio, 'fieldset' );
  const question = queryOne( 'legend.tdp-question-legend', parent_fieldset );
  const answer = queryOne( 'label', radio.parentElement );
  const label = grade_level + ': ' + question.textContent.trim() + ' (' + answer.textContent.trim() + ')';
  if ( sendEventMethod ) {
    return sendEventMethod( action, label );
  }

  /* istanbul ignore next */
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
  if ( link.getAttribute( 'href' ) !== '#' ) {
    return;
  }
  const action = 'Anchor: Missed Question';
  const wrapper = closest( link, 'div.wrapper.tdp-survey' );
  const grade_level = wrapper.getAttribute( 'data-tdp_grade_level' );
  const section = Number( queryOne( 'div[data-page-idx]', wrapper ).getAttribute( 'data-page-idx' ) ) + 1;
  const question = link.textContent.trim();
  const label = grade_level + ': Section ' + section + ' | ' + question;
  if ( sendEventMethod ) {
    return sendEventMethod( action, label );
  }

  /* istanbul ignore next */
  return sendSurveyEvent( action, label );
};

/**
 * handleSurveyRestartModalClick - Listen for Restart survey click and report to GA.
 *
 * @param {event} event Click event
 * @param {method} sendEventMethod method
 * @returns {object} Event data
 */
const handleSurveyRestartModalClick = ( event, sendEventMethod ) => {
  const selector = '[data-open-modal="modal-restart"],[data-open-modal="modal-reset"]';
  const link = closest( event.target, selector );
  let label = '';
  if ( link && link.getAttribute( 'data-open-modal' ) === 'modal-restart' ) {
    const wrapper = closest( link, 'div.wrapper.tdp-survey' );
    const section = Number( queryOne( 'div[data-page-idx]', wrapper ).getAttribute( 'data-page-idx' ) ) + 1;
    const grade_level = wrapper.getAttribute( 'data-tdp_grade_level' );
    label = grade_level + ': Section ' + section;
  } else if ( link && link.getAttribute( 'data-open-modal' ) === 'modal-reset' ) {
    const wrapper = closest( link, 'div.content_wrapper.tdp-survey' );
    const section = 'Results page';
    const grade_level = wrapper.getAttribute( 'data-tdp_grade_level' );
    label = grade_level + ': ' + section;
  } else {
    return;
  }
  const action = 'Start Over';
  if ( sendEventMethod ) {
    return sendEventMethod( action, label );
  }

  /* istanbul ignore next */
  return sendSurveyEvent( action, label );
};

/**
 * handleSurveyExpandableClick - Listen for opening or closing of an expandable and report to GA.
 *
 * @param {event} event Click event
 * @param  {method} sendEventMethod method
 * @returns {object} Event data
 */
const handleSurveyExpandableClick = ( event, sendEventMethod ) => {
  const selector = '.tdp-survey-sidebar__mobile-control .o-expandable_header';
  const expandable = closest( event.target, selector );
  if ( !expandable || !expandable.classList.contains( 'o-expandable_header' ) ) {
    return;
  }
  const state = getExpandableState( expandable ) === 'expand' ? 'Expand' : 'Collapse';
  const action = `Survey Progress Dropdown: ${ state }`;
  const wrapper = closest( expandable, 'div.wrapper.tdp-survey' );
  const grade_level = wrapper.getAttribute( 'data-tdp_grade_level' );
  const section = Number( queryOne( 'div[data-page-idx]', wrapper ).getAttribute( 'data-page-idx' ) ) + 1;
  const label = grade_level + ': Section ' + section;

  if ( sendEventMethod ) {
    return sendEventMethod( action, label );
  }

  /* istanbul ignore next */
  return sendSurveyEvent( action, label );
};

/**
 * handleSurveySectionClick - Listen for Edit Section click and report to GA.
 *
 * @param {event} event Click event
 * @param {method} sendEventMethod method
 * @returns {object} Event data
 */
const handleSurveySectionClick = ( event, sendEventMethod ) => {
  const link = closest( event.target, '[data-editable="1"]' ) || event.target;
  if ( !link.classList.contains( 'tdp-survey-section' ) || ( link.getAttribute( 'data-editable' ) !== '1' ) ) {
    return;
  }
  const action = 'Edit';
  const wrapper = closest( link, 'div.wrapper.tdp-survey' );
  const grade_level = wrapper.getAttribute( 'data-tdp_grade_level' );
  const section = queryOne( '.tdp-survey-section__title', link ).textContent.replace( '(complete)', '' ).trim();
  const label = grade_level + ': ' + section;
  if ( sendEventMethod ) {
    return sendEventMethod( action, label );
  }

  /* istanbul ignore next */
  return sendSurveyEvent( action, label );
};

/**
 * handleSurveySubmitClick - Listen for Submit click and report to GA.
 *
 * @param {event} event Click event
 * @param {method} sendEventMethod method
 * @returns {object} Event data
 */
const handleSurveySubmitClick = ( event, sendEventMethod ) => {
  const link = closest( event.target, 'button.a-btn[type="submit"]' ) || event.target;
  const action = link.textContent.trim();
  if (
    !link.classList.contains( 'a-btn' ) ||
    ( link.getAttribute( 'type' ) !== 'submit' ) ||
    ( action !== 'Get my results' ) ) {
    return;
  }
  const wrapper = closest( link, 'div.wrapper.tdp-survey' );
  const grade_level = wrapper.getAttribute( 'data-tdp_grade_level' );
  const section = Number( queryOne( 'div[data-page-idx]', wrapper ).getAttribute( 'data-page-idx' ) ) + 1;
  const label = grade_level + ': Section ' + section;
  if ( sendEventMethod ) {
    return sendEventMethod( action, label );
  }

  /* istanbul ignore next */
  return sendSurveyEvent( action, label );
};

/**
 * handleSurveyResultsExpandableClick - Listen for opening or closing of an expandable and report to GA.
 *
 * @param {event} event Click event
 * @param  {method} sendEventMethod method
 * @returns {object} Event data
 */
const handleSurveyResultsExpandableClick = ( event, sendEventMethod ) => {
  const selector = '.tdp-survey-results .o-expandable_target';
  const expandable = closest( event.target, selector );
  if ( !expandable || !expandable.classList.contains( 'o-expandable_target' ) ) {
    return;
  }
  const state = getExpandableState( expandable ) === 'expand' ? 'Expand' : 'Collapse';
  const wrapper = closest( expandable, 'div.content_wrapper.tdp-survey' );
  const page_type = queryOne( '.tdp-survey-results--shared', wrapper ) ? 'View' : 'Results';
  const action = `${ page_type } Dropdown: ${ state }`;
  const grade_level = wrapper.getAttribute( 'data-tdp_grade_level' );
  const text = queryOne( '.o-expandable_label', expandable ).textContent.trim();
  const label = grade_level + ': ' + text;

  if ( sendEventMethod ) {
    return sendEventMethod( action, label );
  }

  /* istanbul ignore next */
  return sendSurveyEvent( action, label );
};

/**
 * handleSurveyDownloadClick - Listen for Download link click and report to GA.
 *
 * @param {event} event Click event
 * @param {method} sendEventMethod method
 * @returns {object} Event data
 */
const handleSurveyDownloadClick = ( event, sendEventMethod ) => {
  const link = closest( event.target, '.a-link__icon' ) || event.target;
  if ( !link.classList.contains( 'a-link__icon' ) ) {
    return;
  }
  const action = 'Download';
  const label = link.getAttribute( 'href' );
  if ( sendEventMethod ) {
    return sendEventMethod( action, label );
  }

  /* istanbul ignore next */
  return sendSurveyEvent( action, label );
};

/**
 * handleSurveyResultsModalClick - Listen for Results page Modal click and report to GA.
 *
 * @param {event} event Click event
 * @param {method} sendEventMethod method
 * @returns {object} Event data
 */
const handleSurveyResultsModalClick = ( event, sendEventMethod ) => {
  const selector = '[data-open-modal="modal-print"],[data-open-modal="modal-share-url"]';
  const link = closest( event.target, selector );
  if ( !link || !link.getAttribute( 'data-open-modal' ) ) {
    return;
  }
  const modal_id = link.getAttribute( 'data-open-modal' );
  const action = modal_id === 'modal-print' ? 'Results Print' : 'Results Share';
  const wrapper = closest( link, 'div.content_wrapper.tdp-survey' );
  const grade_level = wrapper.getAttribute( 'data-tdp_grade_level' );
  const label = grade_level;
  if ( sendEventMethod ) {
    return sendEventMethod( action, label );
  }

  /* istanbul ignore next */
  return sendSurveyEvent( action, label );
};

/**
 * handleSurveyResultsModalClose - Listen for Results page Modal click and report to GA.
 *
 * @param {element} modal element
 * @param {element} opener element
 * @returns {object} Event data
 */
const handleSurveyResultsModalClose = ( modal, opener ) => {
  const modal_id = modal.getAttribute( 'id' );
  const wrapper = closest( modal, 'div.content_wrapper.tdp-survey' );
  const valid_ids = [ 'modal-print', 'modal-share-url' ];
  if ( !valid_ids.includes( modal_id ) || !wrapper ) {
    return;
  }
  const action = modal_id === 'modal-print' ? 'Print: Close' : 'Share: Close';

  const grade_level = wrapper.getAttribute( 'data-tdp_grade_level' );
  const label = grade_level;

  return sendSurveyEvent( action, label );
};

/**
 * handleSurveyResultsSavePdfClick - Listen for save as PDF click and report to GA.
 *
 * @param {event} event Click event
 * @param {method} sendEventMethod method
 * @returns {object} Event data
 */
const handleSurveyResultsSavePdfClick = ( event, sendEventMethod ) => {
  const selector = 'a.a-btn[href="/consumer-tools/save-as-pdf-instructions/"]';
  const link = closest( event.target, selector );
  if ( !link ) {
    return;
  }
  const wrapper = closest( link, 'div.content_wrapper.tdp-survey' );
  const grade_level = wrapper.getAttribute( 'data-tdp_grade_level' );
  const page_type = queryOne( '.tdp-survey-results--shared', wrapper ) ? 'View' : 'Results';
  const action = `${ page_type } Save PDF`;
  const label = grade_level;
  if ( sendEventMethod ) {
    return sendEventMethod( action, label );
  }

  /* istanbul ignore next */
  return sendSurveyEvent( action, label );
};

/**
 * handleSurveyResultsGetLinkClick - Listen for Results page Modal Get link click and report to GA.
 *
 * @param {event} event Click event
 * @param {method} sendEventMethod method
 * @returns {object} Event data
 */
const handleSurveyResultsGetLinkClick = ( event, sendEventMethod ) => {
  const link = closest( event.target, '#modal-share-url .tdp-survey__initials-set' );

  if ( !link || !link.classList.contains( 'a-btn' ) ) {
    return;
  }
  const text_field = queryOne( '#modal-share-url input#modal-share-url-initials-input' );
  const action = 'Share: Get Link';
  const wrapper = closest( link, 'div.content_wrapper.tdp-survey' );
  const grade_level = wrapper.getAttribute( 'data-tdp_grade_level' );
  const initials = text_field.value ? 'With initials' : 'No initials';
  const label = grade_level + ': ' + initials;
  if ( sendEventMethod ) {
    return sendEventMethod( action, label );
  }

  /* istanbul ignore next */
  return sendSurveyEvent( action, label );
};

/**
 * handleSurveyResultsGetLinkClick - Listen for Results page Modal Copy link click and report to GA.
 *
 * @param {event} event Click event
 * @param {method} sendEventMethod method
 * @returns {object} Event data
 */
const handleSurveyResultsCopyLinkClick = ( event, sendEventMethod ) => {
  const link = closest( event.target, '#modal-share-url .share-output a, #modal-share-url .share-output button.a-btn' );
  if ( !link ) {
    return;
  }

  const action = 'Share: Copy Link';
  const wrapper = closest( link, 'div.content_wrapper.tdp-survey' );
  const grade_level = wrapper.getAttribute( 'data-tdp_grade_level' );
  const label = grade_level;
  if ( sendEventMethod ) {
    return sendEventMethod( action, label );
  }

  /* istanbul ignore next */
  return sendSurveyEvent( action, label );
};

/**
 * handleSurveyResultsPrintClick - Listen for Results page Modal Print click and report to GA.
 *
 * @param {event} event Click event
 * @param {method} sendEventMethod method
 * @returns {object} Event data
 */
const handleSurveyResultsPrintClick = ( event, sendEventMethod ) => {
  const link = closest( event.target, '#modal-print .tdp-survey__initials-set' );

  if ( !link || !link.classList.contains( 'a-btn' ) ) {
    return;
  }
  const text_field = queryOne( '#modal-print input#modal-print-initials-input' );
  const action = 'Print: Get Link';
  const wrapper = closest( link, 'div.content_wrapper.tdp-survey' );
  const grade_level = wrapper.getAttribute( 'data-tdp_grade_level' );
  const initials = text_field.value ? 'With initials' : 'No initials';
  const label = grade_level + ': ' + initials;
  if ( sendEventMethod ) {
    return sendEventMethod( action, label );
  }

  /* istanbul ignore next */
  return sendSurveyEvent( action, label );
};

/**
 * handleSurveyViewPrintClick - Listen for Results page Modal Print click and report to GA.
 *
 * @param {event} event Click event
 * @param {method} sendEventMethod method
 * @returns {object} Event data
 */
const handleSurveyViewPrintClick = ( event, sendEventMethod ) => {
  const link = closest( event.target, '.tdp-survey-results--shared button[onclick="window.print()"]' );

  if ( !link || !link.classList.contains( 'a-btn' ) ) {
    return;
  }

  const action = 'View Print';
  const wrapper = closest( link, 'div.content_wrapper.tdp-survey' );
  const grade_level = wrapper.getAttribute( 'data-tdp_grade_level' );
  const label = grade_level;
  if ( sendEventMethod ) {
    return sendEventMethod( action, label );
  }

  /* istanbul ignore next */
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
      handleSurveyRestartModalClick( event, sendEventMethod );
      handleSurveyExpandableClick( event, sendEventMethod );
      handleSurveySectionClick( event, sendEventMethod );
      handleSurveySubmitClick( event, sendEventMethod );
      handleSurveyResultsExpandableClick( event, sendEventMethod );
      handleSurveyDownloadClick( event, sendEventMethod );
      handleSurveyResultsModalClick( event, sendEventMethod );
      handleSurveyResultsSavePdfClick( event, sendEventMethod );
      handleSurveyResultsGetLinkClick( event, sendEventMethod );
      handleSurveyResultsCopyLinkClick( event, sendEventMethod );
      handleSurveyResultsPrintClick( event, sendEventMethod );
      handleSurveyViewPrintClick( event, sendEventMethod );
    } );

    surveyContent.addEventListener( 'change', event => {
      handleSurveyChoiceChange( event, sendEventMethod );
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
  handleSurveyRestartModalClick,
  handleSurveyExpandableClick,
  handleSurveySectionClick,
  handleSurveySubmitClick,
  handleSurveyResultsExpandableClick,
  handleSurveyDownloadClick,
  handleSurveyResultsModalClick,
  handleSurveyResultsModalClose,
  handleSurveyResultsSavePdfClick,
  handleSurveyResultsGetLinkClick,
  handleSurveyResultsCopyLinkClick,
  handleSurveyResultsPrintClick,
  handleSurveyViewPrintClick,
  sendEvent,
  sendSurveyEvent,
  bindAnalytics
};
