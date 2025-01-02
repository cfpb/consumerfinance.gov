/* istanbul ignore file */
/* Cypress tests cover all the UI interactions on this page. */

import { addEventListenerToSelector } from '../../../apps/analytics-gtm/js/util/analytics-util';
import { analyticsSendEvent } from '@cfpb/cfpb-analytics';
import search from 'ctrl-f';
import { varsBreakpoints } from '@cfpb/cfpb-design-system';
import { scrollIntoViewWithOffset } from './fig-sidenav-utils.js';

let secondaryNav;
const buttonText = 'Search this guide';

// See https://fusejs.io/api/options.html
const searchOptions = {
  keys: ['contents'],
  includeMatches: true,
  includeScore: true,
  ignoreLocation: true,
  threshold: 0.4,
};

/**
 * Generate a list of structured items to search
 * @param {Array} sections - HTML elements containing FIG headings and
 * paragraphs of content
 * @returns {Array} Structured list of objects to be passed to search engine
 */
const getSearchData = (sections) => {
  if (!sections) return [];
  return sections.map((section, i) => {
    const heading = section.querySelector('.o-fig__heading');
    const link = heading.querySelector('[id]').getAttribute('id');
    const text = section.innerText || section.textContent;
    return {
      id: i,
      title: heading.textContent.replace(/^\s+|\s+$/g, ''),
      contents: text
        .split('\n')
        .map((t) => t.trim())
        .filter((t) => t)
        .join(' '),
      link: '#' + link,
    };
  });
};

/**
 * Event listener that's fired after a user follows a search result.
 * On smaller screens we need to close the TOC before jumping the user
 * to the search result.
 * @param {object} event - Search result follow event
 */
const onFollow = (event) => {
  const target = event.target.closest('a');
  const figLinkID = target.getAttribute('href').replace('#', '');
  const figHeadingLabel = target.querySelector('h4').innerText;

  // Only proceed if the browser window is no greater than 900px
  if (window.matchMedia(`(max-width: ${varsBreakpoints.bpSM.max}px)`).matches) {
    event.preventDefault();
    secondaryNav.collapse();

    // Scrolling before the expandable closes causes jitters on some devices
    setTimeout(() => {
      scrollIntoViewWithOffset(document.getElementById(figLinkID), 60);
    }, 300);
  }

  // Track clicks on individual search results
  analyticsSendEvent({
    event: 'Small Business Lending FIG event',
    action: 'searchresults:click',
    label: figHeadingLabel,
  });
};

/**
 * Event listener that's fired after a user searches for something.
 * We're reporting the user's search terms to Google Analytics.
 * @param {string} query - Search term that was submitted.
 */
const onSubmit = (query) => {
  analyticsSendEvent({
    event: 'Small Business Lending FIG event',
    action: 'search:entry',
    label: query,
  });
};

/**
 * Initialize the ctrl-f search modal.
 * @param {SecondaryNav} secondaryNavArg - A SecondaryNav instance.
 */
function init(secondaryNavArg) {
  secondaryNav = secondaryNavArg;
  // Each searchable item (an HTML section with a heading and some paragraphs)
  // is tagged with a `data-search-section` attribute in the jinja2 template.
  const sectionsList = [...document.querySelectorAll('[data-search-section]')];

  const searchContainer = document.getElementById('ctrl-f');
  const searchData = getSearchData(sectionsList);

  search(searchContainer, {
    buttonText,
    searchOptions,
    searchData,
    onFollow,
    onSubmit,
  });

  // Track clicks on the FIG search form button
  addEventListenerToSelector('#ctrl-f', 'click', () => {
    analyticsSendEvent({
      event: 'Small Business Lending FIG event',
      action: 'search:click',
      label: '',
    });
  });
}

export { init, getSearchData };
