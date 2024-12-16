import { analyticsSendEvent } from '@cfpb/cfpb-analytics';
import { Expandable } from '@cfpb/cfpb-design-system';

let buttonsDom;

/**
 * Changes the visibility of the results by category
 * based on user input
 * @param {string} category - The category to display
 */
function switchComparisons(category) {
  const allCategories = document.querySelectorAll('.comparison__data-point');
  const showCategory = document.querySelectorAll(
    '[class^="comparison__data-point ' + category + '"]',
  );
  const selectedButton = document.querySelector(
    '[data-compare-by="' + category + '"]',
  );
  const selectedButtonClass = 'comparison-chart__toggle-button--selected';
  const hiddenClass = 'u-hidden';

  // Hide all categories ...
  [].forEach.call(allCategories, function (el) {
    el.classList.add(hiddenClass);
  });
  // ... and deselect all toggle buttons ...
  [].forEach.call(buttonsDom, function (el) {
    el.classList.remove(selectedButtonClass);
  });
  // ... so that we can show only the right category data ...
  [].forEach.call(showCategory, function (el) {
    el.classList.remove(hiddenClass);
  });
  // ... and then highlight the correct button.
  selectedButton.classList.add(selectedButtonClass);
}

/**
 * Grabs analytics event data from the passed element's data attributes.
 * Determines the state of the Analytics module and either passes the data
 * or waits for Analytics to report readiness, then passes the data.
 * @param {HTMLElement} el - A dom element
 */
function handleAnalytics(el) {
  const event = el.getAttribute('data-gtm-category');
  const action = el.getAttribute('data-gtm-action');
  const label = el.getAttribute('data-gtm-label');

  analyticsSendEvent({
    event,
    action,
    label,
  });
}

/**
 * Event handler to watch user interaction on each button
 */
function setUpListeners() {
  [].forEach.call(buttonsDom, function (el) {
    el.addEventListener('click', function (event) {
      const input = event.target;

      switchComparisons(input.getAttribute('data-compare-by'));
      handleAnalytics(input);
    });
  });
}

/**
 * Initialize the results interactions
 */
function init() {
  Expandable.init();

  buttonsDom = document.querySelectorAll('.comparison-chart__toggle-button');

  // Sets up the UI for the default age category.
  switchComparisons('age');
  setUpListeners();
}

export default { init };
