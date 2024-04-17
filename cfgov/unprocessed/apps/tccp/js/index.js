import { attach } from '@cfpb/cfpb-atomic-component';

import orderingDropdown from './ordering';
import webStorageProxy from '../../../js/modules/util/web-storage-proxy';

/**
 * Initialize some things.
 */
function init() {
  // Attach "show more" click handler
  attach('show-more', 'click', handleShowMore);
  // Attach landing page location field handler
  attach('select-location', 'change', handleFormValidation);
  // Attach landing page form validation handler
  attach('submit-situations', 'click', handleFormValidation);
  // Make the breadcrumb on the details page go back to a filtered list
  updateBreadcrumb();
  // Move the card ordering dropdown below the expandable
  orderingDropdown.move();
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
 * Prevent form submission if location field isn't completed
 * @param {Event} event - Change/click event.
 */
function handleFormValidation(event) {
  const location = document.querySelector('#id_location');
  const locationError = document.querySelector('#location-required');
  if (location.value) {
    location.classList.remove('a-select--error');
    locationError.classList.add('u-visually-hidden');
  } else {
    event.preventDefault();
    location.closest('.m-form-field').scrollIntoView({ behavior: 'smooth' });
    location.classList.add('a-select--error');
    locationError.classList.remove('u-visually-hidden');
  }
}

/**
 * Update the breadcrumb on the card details page to point back to the filtered
 * list of cards the user came from. We have to do this client-side to prevent
 * Akamai from caching the page with a breadcrumb to a filtered list.
 */
function updateBreadcrumb() {
  const breadcrumb = document.querySelector('.m-breadcrumbs_crumb:last-child');
  if (breadcrumb && breadcrumb.innerText === 'Explore credit cards') {
    breadcrumb.href =
      webStorageProxy.getItem('tccp-filter-path') || breadcrumb.href;
  }
}

window.addEventListener('DOMContentLoaded', () => {
  init();
});
