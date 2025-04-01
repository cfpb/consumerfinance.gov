import { behaviorAttach } from '@cfpb/cfpb-design-system';
import {
  getSearchValues,
  serializeFormFields,
  buildSearchResultsURL,
  showLoading,
  hideLoading,
  handleError,
  updateUrl,
} from './search-utils.js';

// Keep track of the most recent XHR request so that we can cancel it if need be
const searchRequest = new AbortController();
const { signal } = searchRequest.signal;

/**
 * Initialize search functionality.
 */
function init() {
  // Override search form submission
  behaviorAttach('submit-search', 'submit', handleSubmit);
  behaviorAttach('change-filter', 'change', handleFilter);
  attachHandlers();
}

/**
 * Attach search results handlers
 */
function attachHandlers() {
  behaviorAttach('clear-filter', 'click', clearFilter);
  behaviorAttach('clear-all', 'click', clearFilters);
}

/**
 * Remove a filter from the search results page.
 * @param {Event} event - Click event.
 */
function clearFilter(event) {
  const target = event.currentTarget;
  const checkbox = document.querySelector(
    `#regulation-${target.getAttribute('data-value')}`,
  );
  // Remove the filter tag
  removeTag(target);
  // Uncheck the filter checkbox
  checkbox.checked = false;
  if (event instanceof Event) {
    handleFilter(event);
  }
}

/**
 * Remove a filter tag from the search results page.
 * node.remove() isn't supported by IE so we have to removeChild();
 * @param {Node} tag - Filter tag HTML element.
 */
function removeTag(tag) {
  if (tag.parentNode !== null) {
    tag.parentNode.removeChild(tag);
  }
}

/**
 * Remove all filters from the search results page.
 * @param {Event} event - Click event.
 */
function clearFilters(event) {
  const filterTags = document.querySelectorAll('.filters__tags .a-tag-filter');
  filterTags.forEach((filterTag) => {
    clearFilter({
      currentTarget: filterTag,
    });
  });
  handleFilter(event);
}

/**
 * Handle keyword search form submission.
 * @param {Event} event - Click event.
 * @returns {string} New page URL with search terms.
 */
function handleSubmit(event) {
  if (event instanceof Event) {
    event.preventDefault();
  }
  const filters = document.querySelectorAll('input:checked');
  const searchField = document.querySelector('input[name=q]');
  const searchTerms = getSearchValues(searchField, filters);
  const baseUrl = window.location.href.split('?')[0];
  const searchParams = serializeFormFields(searchTerms);
  const searchUrl = buildSearchResultsURL(baseUrl, searchParams);
  window.location.assign(searchUrl);
  return searchUrl;
}

/**
 * Handle filter change events.
 * @param {Event} event - Click event.
 */
function handleFilter(event) {
  if (event instanceof Event) {
    event.preventDefault();
  }
  // Abort the previous search request if it's still active
  /* eslint no-empty: ["error", { "allowEmptyCatch": true }] */
  try {
    searchRequest.abort();
  } catch {}
  const searchContainer = document.querySelector('#regs3k-results');
  const filters = document.querySelectorAll('input:checked');
  const searchField = document.querySelector('input[name=q]');
  const searchTerms = getSearchValues(searchField, filters);
  const baseUrl = window.location.href.split('?')[0];
  const searchParams = serializeFormFields(searchTerms);
  const searchUrl = buildSearchResultsURL(baseUrl, searchParams, {
    partial: true,
  });

  // Update the filter query params in the URL
  updateUrl(baseUrl, searchParams);
  showLoading(searchContainer);
  fetch(searchUrl, { signal })
    .then((response) => response.text())
    .then((data) => {
      hideLoading(searchContainer);
      searchContainer.innerHTML = data;
      // Update the query params in the URL
      updateUrl(baseUrl, searchParams);
      // Reattach event handlers after tags are reloaded
      attachHandlers();
    })
    .catch((err) => {
      // TODO: Add message banner above search results
      console.error(handleError(err).msg);
    });
}

// Provide the no-JS experience to browsers without `replaceState`
if ('replaceState' in window.history) {
  window.addEventListener('load', () => {
    init();
  });
} else {
  document.getElementById('main').className += ' no-js';
}
