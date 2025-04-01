import { analyticsSendEvent } from '@cfpb/cfpb-analytics';
import { behaviorAttach } from '@cfpb/cfpb-design-system';
import { Tooltip } from '@cfpb/cfpb-design-system/tooltips';

import orderingDropdown from './ordering';
import webStorageProxy from '../../../js/modules/util/web-storage-proxy';

let tooltips;

/**
 * Initialize some things.
 */
function init() {
  // Attach "show more" click handler
  behaviorAttach('show-more', 'click', handleShowMore);
  // Attach change handler to the "sort by" field
  behaviorAttach('ordering-change', 'change', handleOrderingChange);
  // Attach landing page location field handler
  behaviorAttach('select-location', 'change', handleFormValidation);
  // Attach landing page form validation handler
  behaviorAttach('submit-situations', 'click', handleFormValidation);
  // Attach handler for conditional link targets
  behaviorAttach('ignore-link-targets', 'click', handleIgnoreLinkTargets);
  // Attach handler for "Enter" on card details link proxy
  behaviorAttach('card-link-proxy', 'keydown', handleCardLinkProxies);
  // Make the breadcrumb on the details page go back to a filtered list
  updateBreadcrumb();
  // Move the card ordering dropdown below the expandable
  orderingDropdown.move();
  // Initialize any tooltips on the page
  tooltips = Tooltip.init();
  // Reinitialize tooltips after an htmx request replaces DOM nodes
  behaviorAttach(document, 'htmx:afterSwap', initializeAndReport);
}

/**
 *
 * @param {Event} event - htmx event
 */
function initializeAndReport(event) {
  tooltips = Tooltip.init();
  reportFilter(event);
  // Attach handler for "Enter" on card details link proxy
  behaviorAttach('card-link-proxy', 'keydown', handleCardLinkProxies);
}

/**
 *
 * @param {Event} event - htmx event
 */
function reportFilter(event) {
  let category, value;
  const { target } = event.detail.requestConfig.triggeringEvent;
  if (target.tagName === 'SELECT') {
    category = target.name;
    value = target.value;
  } else {
    category = target
      .closest('fieldset')
      .firstElementChild.textContent.toLowerCase();
    value = target.labels[0].textContent.trim();
  }

  analyticsSendEvent({
    event: 'tccp:card-list-refinement',
    category,
    value,
  });
}

/**
 * Handle links that shouldn't be followed when
 * specified children elements are targeted
 * or a tooltip is open.
 * @param {Event} event - Touch/click event.
 */
function handleIgnoreLinkTargets(event) {
  const ignoredTargets = event.currentTarget?.getAttribute(
    'data-ignore-link-targets',
  );
  const tooltipIsOpen = tooltips.some((tip) => tip.tooltip.state.isMounted);

  if (event.target.closest(ignoredTargets) || tooltipIsOpen) {
    event.preventDefault();
  }
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
  const showMoreFade = document.querySelector('#u-show-more-fade');
  const nextResult = document.querySelector(
    '[data-js-hook="behavior_faded-card"]',
  );
  nextResult.setAttribute('tabIndex', '0');
  nextResult.querySelectorAll('[tabindex="-1"]').forEach((elem) => {
    elem.setAttribute('tabIndex', '0');
  });
  results.classList.remove('o-filterable-list-results--partial');
  showMoreFade.classList.add('u-hidden');
  nextResult.focus();
}

/**
 * Handle display of "show more" link when ordering is changed.
 * It shouldn't be shown when ordering by product name.
 * @param {Event} event - Click event.
 */
function handleOrderingChange(event) {
  const results = document.querySelector('.o-filterable-list-results');
  const showMoreFade = document.querySelector('#u-show-more-fade');
  if (event.target && event.target.value === 'product_name') {
    results.classList.remove('o-filterable-list-results--partial');
    showMoreFade.classList.add('u-hidden');
  } else {
    results.classList.add('o-filterable-list-results--partial');
    showMoreFade.classList.remove('u-hidden');
  }
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
 * Handles "Enter" key on focusable p elements ("card link proxies"). These
 * proxies are p elements masquerading as anchor tags.
 * @param {Event} event - Keydown event
 */
function handleCardLinkProxies(event) {
  if (event.key && event.key === 'Enter') {
    const parentAnchor = event.target.closest('a');
    parentAnchor.click();
  }
}

/**
 * Update the breadcrumb on the card details page to point back to the filtered
 * list of cards the user came from. We have to do this client-side to prevent
 * Akamai from caching the page with a breadcrumb to a filtered list.
 */
function updateBreadcrumb() {
  const breadcrumb = document.querySelector('.m-breadcrumbs__crumb:last-child');
  if (breadcrumb && breadcrumb.innerText === 'Explore credit cards') {
    breadcrumb.href =
      webStorageProxy.getItem('tccp-filter-path') || breadcrumb.href;
  }
}

window.addEventListener('DOMContentLoaded', () => {
  init();
});
