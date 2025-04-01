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
import expandableFacets from './expandable-facets.js';
import cfExpandables from './Expandable.js';
import {
  handleClearAllClick,
  handleFetchSearchResults,
} from './tdp-analytics.js';

// Keep track of the most recent XHR request so that we can cancel it if need be
const searchRequest = new AbortController();
const { signal } = searchRequest.signal;

/**
 * Initialize search functionality.
 */
function init() {
  if ('replaceState' in window.history) {
    // Override search form submission
    attachHandlers();
  } else {
    // This case already handled inline at the bottom
  }
}

/**
 * Attach search results handlers
 */
function attachHandlers() {
  addDataGtmIgnore();
  behaviorAttach('submit-search', 'submit', handleSubmit);
  behaviorAttach('change-filter', 'change', handleFilter);
  behaviorAttach('clear-filter', 'click', clearFilter);
  behaviorAttach('clear-all', 'click', clearFilters);
  cfExpandables.init();
  expandableFacets.init();
}

/**
 * Ignore analytics for previous and next pagination buttons
 */
function addDataGtmIgnore() {
  const ignoreBtns = ['a.m-pagination__btn-next', 'a.m-pagination__btn-prev'];

  for (let i = 0; i < ignoreBtns.length; i++) {
    const btn = document.querySelector(ignoreBtns[i]);
    if (btn) {
      btn.setAttribute('data-gtm_ignore', 'true');
    }
  }
}

/**
 * Remove a filter from the search results page.
 * @param {Event} event - Click event
 */
function clearFilter(event) {
  const target = event.currentTarget;
  const checkbox = document.querySelector(target.getAttribute('data-value'));
  // Remove the filter tag
  removeTag(target);
  // Uncheck the filter checkbox
  checkbox.checked = false;
  if (event instanceof Event) {
    handleFilter(event, checkbox);
  }
}

/**
 * Remove a filter tag from the search results page.
 * node.remove() isn't supported by IE so we have to removeChild();
 * @param {Node} tag - Filter tag HTML element
 */
function removeTag(tag) {
  if (tag.parentNode !== null) {
    tag.parentNode.removeChild(tag);
  }
}

/**
 * Remove all filters from the search results page.
 * @param {Event} event - Click event
 */
function clearFilters(event) {
  // Handle Analytics here before tags vanish.
  handleClearAllClick(event);

  const filterTags = document.querySelectorAll('.a-tag-filter');
  filterTags.forEach((filterTag) => {
    clearFilter({
      currentTarget: filterTag,
    });
  });
  clearSearch();
}

/**
 * Trigger a form submit after Clear Search is clicked.
 */
function clearSearch() {
  document.querySelector('input[name=q]').value = '';
  handleSubmit(event);
}

/**
 * Handle keyword search form submission.
 * @param {Event} event - Click event
 * @returns {string} New page URL with search terms
 */
function handleSubmit(event) {
  if (event instanceof Event) {
    event.preventDefault();
  }
  const filters = document.querySelectorAll('input:checked');
  // fetch search results without applying filters when searching
  const searchUrl = fetchSearchResults(filters);
  return searchUrl;
}

/**
 * fetch search results based on filters and keywords.
 * @param {NodeList} filters - List of filter checkboxes
 * @returns {string} New page URL with search terms
 */
function fetchSearchResults(filters = []) {
  const searchContainer = document.querySelector(
    '#tdp-search-facets-and-results',
  );
  const baseUrl = window.location.href.split('?')[0];
  const searchField = document.querySelector('input[name=q]');
  const searchTerms = getSearchValues(searchField, filters);
  const searchParams = serializeFormFields(searchTerms);

  const searchUrl = buildSearchResultsURL(baseUrl, searchParams);

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

      // Send search query to Analytics.
      handleFetchSearchResults(searchField.value);
    })
    .catch((err) => {
      // TODO: Add message banner above search results
      console.error(handleError(err).msg);
    });

  return searchUrl;
}

/**
 * Handle filter change events.
 * @param {Event} event - Click event
 * @param {HTMLElement} target - DOM element
 * @returns {string} New page URL with search terms
 */
function handleFilter(event, target = null) {
  if (event instanceof Event) {
    event.preventDefault();
  }
  // Abort the previous search request if it's still active
  /* eslint no-empty: ["error", { "allowEmptyCatch": true }] */
  try {
    searchRequest.abort();
  } catch {}
  target = target ? target : event.target;
  const wrapperLI = target.parentElement.parentElement;
  if (wrapperLI && wrapperLI.tagName.toLowerCase() === 'li') {
    // Check all children if parent is checked.
    const checkboxes = wrapperLI.querySelectorAll('ul>li input[type=checkbox]');
    for (let i = 0; i < checkboxes.length; i++) {
      if (
        wrapperLI.contains(checkboxes[i]) === true &&
        checkboxes[i] !== target
      ) {
        checkboxes[i].checked = target.checked;
      }
    }
    // If this is a child checkbox, update the parent checkbox.
    const parentLI = wrapperLI.parentElement.parentElement;
    const parentUL = wrapperLI.parentElement.parentElement.parentElement;
    if (parentUL && parentUL.tagName.toLowerCase() === 'ul') {
      const parentCheckbox = parentLI.querySelector('div>input[type=checkbox]');
      if (
        parentCheckbox &&
        parentCheckbox.parentElement.parentElement === parentLI
      ) {
        _updateParentFilter(parentCheckbox);
      }
    }
  }

  const filters = document.querySelectorAll('input:checked');
  const searchUrl = fetchSearchResults(filters);
  return searchUrl;
}

/**
 * Traverse parents and update their checkbox values.
 * @param {HTMLElement} element - DOM element
 */
function _updateParentFilter(element) {
  const wrapper = element.parentElement.parentElement;
  const checkboxes = wrapper.querySelectorAll('ul>li input[type=checkbox]');

  const children = [];
  const checkedChildren = [];
  for (let i = 0; i < checkboxes.length; i++) {
    if (wrapper.contains(checkboxes[i]) === true) {
      children.push(checkboxes[i]);
      if (checkboxes[i].checked === true) {
        checkedChildren.push(checkboxes[i]);
      }
    }
  }

  if (children) {
    if (children.length !== checkedChildren.length) {
      element.checked = false;
    }
  }
  // Loop through ancestors and make sure they are checked or unchecked
  const parentWrapper = wrapper.parentElement.parentElement;
  const parentCheckbox = parentWrapper.querySelector(
    'div>input[type=checkbox]',
  );
  if (parentCheckbox && parentCheckbox.parentElement === parentWrapper) {
    _updateParentFilter(parentCheckbox);
  }
}

// Provide the no-JS experience to browsers without `replaceState`
if ('replaceState' in window.history) {
  // This case handled in init() above
} else {
  document.getElementById('main').className += ' no-js';
}

export { init };
