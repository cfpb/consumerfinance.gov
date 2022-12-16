/* istanbul ignore file */
/* Cypress tests cover all the UI interactions on this page. */

import search from 'ctrl-f';
import varsBreakpoints from '@cfpb/cfpb-core/src/vars-breakpoints.js';
import { scrollIntoViewWithOffset } from './fig-sidenav-utils.js';

const buttonText = 'Search this guide';

// See https://fusejs.io/api/options.html
const searchOptions = {
  keys: ['contents'],
  includeMatches: true,
  includeScore: true,
  ignoreLocation: true,
  threshold: 0.4,
};

function init() {
  // Each searchable item (an HTML section with a heading and some paragraphs)
  // is tagged with a `data-search-section` attribute in the jinja2 template.
  const sectionsList = [...document.querySelectorAll('[data-search-section]')];

  const searchContainer = document.getElementById('ctrl-f');
  const searchData = getSearchData(sectionsList);

  search(searchContainer, { buttonText, searchOptions, searchData, onFollow });
}

/**
 * Generate a list of structured items to search
 *
 * @param {Array} sections - HTML elements containing FIG headings and
 * paragraphs of content
 * @returns {Array} Structured list of objects to be passed to search engine
 */
const getSearchData = (sections) => {
  if (!sections) return [];
  return sections.map((section, i) => {
    const heading = section.querySelector('.o-fig_heading');
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
 *
 * @param {object} event - Search result follow event
 */
const onFollow = (event) => {
  // Only proceed if the browser window is no greater than 900px
  if (
    window.matchMedia(`(max-width: ${varsBreakpoints.bpSM.max}px)`).matches
  ) {
    event.preventDefault();
    const target = event.target
      .closest('a')
      .getAttribute('href')
      .replace('#', '');
    document
      .querySelector('.o-fig_sidebar button.o-expandable_header')
      .click();
    // Scrolling before the expandable closes causes jitters on some devices
    setTimeout(() => {
      scrollIntoViewWithOffset(document.getElementById(target), 60);
    }, 300);
  }
};

export { init, getSearchData };
