import { analyticsSendEvent } from '@cfpb/cfpb-analytics';

let searchContent;

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
  let el = event.target.closest('.o-expandable__header');
  el = el ? el : event.target.closest('.o-expandable-facets__target');
  el = el ? el : event.target;

  if (
    el.classList.contains('o-expandable__header') ||
    el.classList.contains('o-expandable-facets__target')
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
    expandable.classList.contains('o-expandable__target--expanded') ||
    expandable.classList.contains('is-open')
  ) {
    state = 'expand';
  }
  return state;
};

/**
 * Old analytics (UA). TODO: Remove when completely on GA4.
 *
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
  let label = expandable.querySelector('span.o-expandable__label');
  label = label ? label : expandable.querySelector('span[aria-hidden=true]');
  if (!label) {
    return;
  }
  label = label.textContent.trim();

  return sendEvent({
    event: 'TDP Search Tool',
    action: action,
    label: label,
  });
};

/**
 * handleFilterClick - Listen for filter clicks and report to GA.
 * @param {event} event - Click event.
 * @returns {object|undefined} Event data.
 */
const handleFilterClick = (event) => {
  const filters = event.currentTarget.querySelector('.filters');
  if (!filters) return;
  const checkbox = filters.closest('.a-checkbox') || event.target;
  if (!checkbox.classList.contains('a-checkbox')) {
    return;
  }
  const action = checkbox.checked ? 'filter' : 'remove filter';
  const label = checkbox.getAttribute('aria-label');

  // Old analytics. TODO: Remove when completely on GA4.
  sendEvent({
    event: 'TDP Search Tool',
    action: action,
    label: label,
  });

  // GA4.
  return sendEvent({
    event: 'filter',
    action,
    label,
  });
};

/**
 * handleClearFilterClick - Listen for clear filter clicks and report to GA.
 * @param {event} event - Click event.
 * @returns {object|undefined} Event data.
 */
const handleClearFilterClick = (event) => {
  const tags = event.currentTarget.querySelector('.results__filters-tags');
  if (!tags) return;
  const tag = tags.closest('.a-tag-filter') || event.target;
  if (!tag.classList.contains('a-tag-filter')) {
    return;
  }

  const action = 'remove filter';
  const label = tag.textContent.trim();

  // Old analytics. TODO: Remove when completely on GA4.
  sendEvent({
    event: 'TDP Search Tool',
    action: action,
    label: label,
  });

  // GA4.
  return sendEvent({
    event: 'filter',
    action,
    label,
  });
};

/**
 * handlePaginationClick - Listen for pagination clicks and report to GA.
 * @param {event} event - Click event.
 * @returns {object|undefined} Event data.
 */
const handlePaginationClick = (event) => {
  const paginator = event.target.closest('.a-btn') || event.target;
  if (!paginator.classList.contains('a-btn')) {
    return;
  }

  const isNextButton = paginator.classList.contains('m-pagination__btn-next');
  const isPrevButton = paginator.classList.contains('m-pagination__btn-prev');
  const isGoButton = paginator.classList.contains('m-pagination__btn-submit');
  const isDisabled = paginator.classList.contains('a-btn--disabled');

  if (isDisabled || (!isNextButton && !isPrevButton && !isGoButton)) {
    return;
  }

  const currPageDom = searchContent.querySelector(
    '.m-pagination__current-page',
  );

  // This is the actual page number we're on.
  const currPage = parseInt(currPageDom.getAttribute('value'), 10);
  // This is the page that's set in the page counter.
  const selPage = parseInt(currPageDom.value, 10);
  const ofTotalPagesTxt = searchContent.querySelectorAll(
    '.m-pagination__label',
  )[1].textContent;
  let usePage = currPage;

  let action;
  if (isNextButton) {
    action = 'next page';
  } else if (isPrevButton) {
    action = 'previous page';
  } else if (isGoButton) {
    action = 'goto page';
    usePage = selPage;
  }

  const label = `page ${usePage}${ofTotalPagesTxt}`;

  // Old analytics. TODO: Remove when completely on GA4.
  sendEvent({
    event: 'TDP Search Tool',
    action: action,
    label: label,
  });

  // GA4.
  return sendEvent({
    event: 'pagination',
    action,
    label,
  });
};

/**
 * handleClearAllClick - Listen for clear all filters clicks and report to GA.
 * @param {event} event - Click event.
 * @returns {object|undefined} Event data.
 */
const handleClearAllClick = (event) => {
  const clearBtn = event.currentTarget;
  const tagsWrapper = clearBtn.parentElement;
  const tags = tagsWrapper.querySelectorAll('.a-tag-filter');
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
    action: 'clear all filters',
    label: tagNames.join(' | '),
  });

  // GA4.
  return sendEvent({
    event: 'clear_all_filters',
    label: tagNames.join(' | '),
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
  const resultsCountBlock = searchContent.querySelector('.results__count');
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
        search_term: searchTerm.toLowerCase(),
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

  searchContent = document.querySelector('#tdp-search-facets-and-results');

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
