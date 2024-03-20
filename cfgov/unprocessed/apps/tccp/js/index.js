import htmx from 'htmx.org';
import { attach } from '@cfpb/cfpb-atomic-component';

// See https://htmx.org/docs/#caching
htmx.config.getCacheBusterParam = true;

/**
 * Initialize some things.
 */
function init() {
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
