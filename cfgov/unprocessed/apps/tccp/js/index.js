import { attach } from '@cfpb/cfpb-atomic-component';

import webStorageProxy from '../../../js/modules/util/web-storage-proxy';

/**
 * Initialize some things.
 */
function init() {
  // Store the card filter query params to web storage for our breadcrumbs
  webStorageProxy.setItem('tccp-filter-path', window.location.pathname);
  // Attach "show more" click handler
  attach('show-more', 'click', handleShowMore);
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

window.addEventListener('load', () => {
  init();
});
