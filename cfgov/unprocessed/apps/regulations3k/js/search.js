import { attach } from '../../../js/modules/util/behavior.js';
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
  attach('submit-search', 'submit', handleSubmit);
  attach('change-filter', 'change', handleFilter);
  attachHandlers();
}

/**
 * Attach search results handlers
 */
function attachHandlers() {
  attach('clear-filter', 'click', clearFilter);
  attach('clear-all', 'click', clearFilters);
}

/**
 * Remove a filter from the search results page.
 *
 * @param {Event} event - Click event.
 */
function clearFilter(event) {
  // Continue only if the X icon was clicked and not the parent button
  let target = event.target.tagName.toLowerCase();
  if (target !== 'svg' && target !== 'path') {
    return;
  }
  target = event.target.closest('.a-tag');
  const checkbox = document.querySelector(
    `#regulation-${target.getAttribute('data-value')}`
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
 *
 * @param {Node} tag - Filter tag HTML element.
 */
function removeTag(tag) {
  if (tag.parentNode !== null) {
    tag.parentNode.removeChild(tag);
  }
}

/**
 * Remove all filters from the search results page.
 *
 * @param {Event} event - Click event.
 */
function clearFilters(event) {
  let filterIcons = document.querySelectorAll('.filters_tags svg');
  // IE doesn't support forEach w/ node lists so convert it to an array.
  filterIcons = Array.prototype.slice.call(filterIcons);
  filterIcons.forEach((filterIcon) => {
    const target = filterIcon.closest('.a-tag');
    clearFilter({
      target: filterIcon,
      value: target,
    });
  });
  handleFilter(event);
}

/**
 * Handle keyword search form submission.
 *
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
 *
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
  } catch (err) {}
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
