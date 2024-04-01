import { attach } from '@cfpb/cfpb-atomic-component';

import webStorageProxy from '../../../js/modules/util/web-storage-proxy';

/**
 * Initialize some things.
 */
function init() {
  // Attach "show more" click handler
  attach('show-more', 'click', handleShowMore);
  // Make the breadcrumb on the details page go back to a filtered list
  updateBreadcrumb();
  // Move the card ordering dropdown below the expandable
  moveOrderingDropdown();
}

/**
 * Handle clicking of the results page "show more" link
 * @param {Event} event - Click event.
 */
function handleShowMore(event) {
  if (event instanceof Event) {
    event.preventDefault();
  }
  const results = document.querySelector('.o-filterable-list-results');
  results.classList.remove('o-filterable-list-results__partial');

  event.target.classList.add('u-hidden');
}

/**
 * Update the breadcrumb on the card details page to point back to the filtered
 * list of cards the user came from. We have to do this client-side to prevent
 * Akamai from caching the page with a breadcrumb to a filtered list.
 */
function updateBreadcrumb() {
  const breadcrumb = document.querySelector('.m-breadcrumbs_crumb:last-child');
  if (breadcrumb.innerText === 'Customize for your situation') {
    breadcrumb.href =
      webStorageProxy.getItem('tccp-filter-path') || breadcrumb.href;
  }
}

/**
 * Moves the card ordering dropdown outside the filters' expandable to
 * improve its visibility. Doing this via JS instead of at the template
 * level preserves the HTML form for no-JS users.
 */
function moveOrderingDropdown() {
  const orderingDropdown = document.querySelector('#tccp-ordering');
  document.querySelector('#tccp-ordering-container').append(orderingDropdown);
}

window.addEventListener('DOMContentLoaded', () => {
  init();
});
