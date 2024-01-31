import { analyticsSendEvent } from '@cfpb/cfpb-analytics';

/**
 * Sends the user interaction to Analytics
 * @param {object} payload - Payload of arbitrary key/value analytics data.
 * @returns {object} Event data
 */
let sendEvent = (payload) => {
  analyticsSendEvent(payload);
  return payload;
};

/**
 * getExpandable - Find the expandable the user clicked.
 * @param {event} event - Click event
 * @returns {HTMLElement|null} The expandable or null if it's not an expandable
 */
const getExpandable = (event) => {
  let el = event.target.closest('.o-expandable_header');
  el = el ? el : event.target.closest('.o-expandable-facets_target');
  el = el ? el : event.target;

  if (
    el.classList.contains('o-expandable_header') ||
    el.classList.contains('o-expandable-facets_target')
  ) {
    return el;
  }
  return null;
};

/**
 * getExpandableState - Description
 * @param {HTMLElement} expandable - Expandable's HTML element
 * @returns {string} Expandable's state, either `open` or `close`
 */
const getExpandableState = (expandable) => {
  let state = 'collapse';
  if (
    expandable.classList.contains('o-expandable_target__expanded') ||
    expandable.classList.contains('is-open')
  ) {
    state = 'expand';
  }
  return state;
};

/**
 * handleExpandableClick - Listen for clicks within a search page's content
 * and report to GA if they opened or closed an expandable.
 * @param {event} event - Click event.
 * @returns {object|undefined} Event data.
 */
const handleExpandableClick = (event) => {
  const expandable = getExpandable(event);
  if (!expandable) {
    return;
  }
  const action = `${getExpandableState(expandable)} filter`;
  let label = expandable.querySelector('span.o-expandable_label');
  label = label ? label : expandable.querySelector('span[aria-hidden=true]');
  if (!label) {
    return;
  }
  label = label.textContent.trim();

  return sendEvent(action, label);
};

/**
 * handleFilterClick - Listen for filter clicks and report to GA.
 * @param {event} event - Click event.
 * @returns {object|undefined} Event data.
 */
const handleFilterClick = (event) => {
  const checkbox = event.target;
  if (!checkbox.classList.contains('a-checkbox')) {
    return;
  }
  const action = checkbox.checked ? 'filter' : 'remove filter';
  const label = checkbox.getAttribute('aria-label');

  return sendEvent(action, label);
};

/**
 * handleClearFilterClick - Listen for clear filter clicks and report to GA.
 * @param {event} event - Click event.
 * @returns {object|undefined} Event data.
 */
const handleClearFilterClick = (event) => {
  // Continue only if the X icon was clicked and not the parent button
  let target = event.target.tagName.toLowerCase();
  if (target !== 'svg' && target !== 'path') {
    return;
  }
  target = event.target.closest('.a-tag[data-js-hook=behavior_clear-filter]');

  if (!target) {
    return;
  }
  const action = 'remove filter';
  const label = target.textContent.trim();

  return sendEvent(action, label);
};

/**
 * getPaginator - Find the paginator the user clicked.
 * @param {event} event - Click event
 * @returns {HTMLElement|null} The checkbox div or null if it's not a checkbox
 */
const getPaginator = (event) => {
  const el = event.target.closest('.a-btn') || event.target;
  if (el.classList.contains('a-btn')) {
    return el;
  }
  return null;
};

/**
 * handlePaginationClick - Listen for pagination clicks and report to GA.
 * @param {event} event - Click event.
 * @returns {object|undefined} Event data.
 */
const handlePaginationClick = (event) => {
  const paginator = getPaginator(event);
  if (!paginator) {
    return;
  }

  const isNextButton = paginator.classList.contains('m-pagination_btn-next');
  const isPrevButton = paginator.classList.contains('m-pagination_btn-prev');
  const isDisabled = paginator.classList.contains('a-btn__disabled');

  if (!paginator.href || isDisabled || (!isNextButton && !isPrevButton)) {
    return;
  }

  const action = isNextButton ? 'next page' : 'previous page';
  let label = paginator.href.match(/\?.*page=(\d+)/);
  if (!label) {
    return;
  }
  label = isNextButton
    ? parseInt(label[1], 10) - 1
    : parseInt(label[1], 10) + 1;
  return sendEvent(action, label);
};

/**
 * getClearBtn - Find the clear all filters button.
 * @param {event} event - Click event
 * @returns {HTMLElement|null} The checkbox div or null if it's not a checkbox
 */
const getClearBtn = (event) => {
  const el = event.target.closest('.results_filters-clear') || event.target;
  if (el.classList.contains('results_filters-clear')) {
    return el;
  }
  return null;
};

/**
 * handleClearAllClick - Listen for clear all filters clicks and report to GA.
 * @param {event} event - Click event.
 * @returns {object|undefined} Event data.
 */
const handleClearAllClick = (event) => {
  const clearBtn = getClearBtn(event);
  if (!clearBtn) {
    return;
  }
  const tagsWrapper = clearBtn.parentElement;
  const tags = tagsWrapper.querySelectorAll('.a-tag');
  if (!tags || tags.length === 0) {
    return;
  }
  const tagNames = [];
  for (let i = 0; i < tags.length; i++) {
    if (tagsWrapper.contains(tags[i])) {
      tagNames.push(tags[i].textContent.trim());
    }
  }
  if (tagNames.length === 0) {
    return;
  }

  // Old analytics. TODO: Remove when completely on GA4.
  sendEvent({
    event: 'TDP Search Tool',
    action: 'remove filter',
    label: target.textContent.trim(),
  });

  // GA4.
  return sendEvent({
    event: 'clear_button_click',
    button_label: tagNames.join('|'),
  });
};

/**
 * handleFetchSearchResults - Listen for AJAX fetchSearchResults
 * and report to GA.
 * @param {string} searchTerm - string.
 */
const handleFetchSearchResults = (searchTerm) => {
  if (searchTerm.length === 0) {
    return;
  }

  // Send the keywords that return 0 results to Analytics.
  const resultsCountBlock = document.querySelector(
    '#tdp-search-facets-and-results .results_count',
  );
  if (resultsCountBlock) {
    const resultsCount = resultsCountBlock.getAttribute('data-results-count');

    // Check if result count is 0
    if (resultsCount === '0') {
      // Old analytics. TODO: Remove when completely on GA4.
      sendEvent({
        event: 'TDP Search Tool',
        action: 'noSearchResults',
        label: searchTerm.toLowerCase() + ':0',
      });

      // GA4.
      sendEvent({
        event: 'search',
        search_term: searchTerm.toLowerCase() + ':0',
        results_count: 0,
        no_search_results: true,
      });
    } else {
      // Old analytics. TODO: Remove when completely on GA4.
      sendEvent({
        event: 'TDP Search Tool',
        action: 'search',
        label: searchTerm.toLowerCase(),
      });

      // GA4.
      sendEvent({
        event: 'search',
        search_term: searchTerm.toLowerCase(),
        results_count: resultsCount,
        no_search_results: false,
      });
    }
  }
};

/**
 * bindAnalytics - Set up analytics reporting.
 * @param {Function} spyMethod - optional spy method.
 */
const bindAnalytics = (spyMethod) => {
  if (spyMethod) {
    // TODO: sendEvent exists so it can be mocked in the unit tests.
    //       Look into rewriting the tests to mock analyticsSendEvent.
    sendEvent = spyMethod;
  }

  const searchContent = document.querySelector(
    '#tdp-search-facets-and-results',
  );
  if (searchContent) {
    searchContent.addEventListener('click', (event) => {
      handleExpandableClick(event);
      handleFilterClick(event);
      handleClearFilterClick(event);
      handlePaginationClick(event);
    });
  }
};

export { handleClearAllClick, handleFetchSearchResults, bindAnalytics };
