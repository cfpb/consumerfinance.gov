import fetchMock from 'jest-fetch-mock';
fetchMock.enableMocks();
import { jest } from '@jest/globals';
import { simulateEvent } from '../../../../util/simulate-event.js';

import '../../../../../cfgov/unprocessed/apps/regulations3k/js/search.js';

const HTML_SNIPPET = `
  <form action="/search" data-js-hook="behavior_submit-search">
    <div class="o-search-input">
      <div class="o-search-input__input">
          <label for="query" class="o-search-input__input-label" aria-label="Search for a term">
              <svg xmlns="http://www.w3.org/2000/svg" class="cf-icon-svg cf-icon-svg--search" viewBox="0 0 15 19"><path d="M14.147 15.488a1.11 1.11 0 0 1-1.567 0l-3.395-3.395a5.575 5.575 0 1 1 1.568-1.568l3.394 3.395a1.11 1.11 0 0 1 0 1.568m-6.361-3.903a4.488 4.488 0 1 0-1.681.327 4.4 4.4 0 0 0 1.68-.327z"></path></svg>
          </label>
          <input type="search" id="query" name="q" value="money" class="a-text-input a-text-input__full" placeholder="Enter your search term" title="Enter your search term" autocomplete="off" maxlength="75">
          <button type="reset" onclick="document.getElementById('query').setAttribute('value','')" aria-label="Clear search" title="Clear search">
                  <svg xmlns="http://www.w3.org/2000/svg" class="cf-icon-svg cf-icon-svg--error" viewBox="0 0 12 19"><path d="M11.383 13.644A1.03 1.03 0 0 1 9.928 15.1L6 11.172 2.072 15.1a1.03 1.03 0 1 1-1.455-1.456l3.928-3.928L.617 5.79a1.03 1.03 0 1 1 1.455-1.456L6 8.261l3.928-3.928a1.03 1.03 0 0 1 1.455 1.456L7.455 9.716z"></path></svg>
          </button>
      </div>

      <button class="a-btn" type="submit" aria-label="Search for a term in the regulations">
          Search
      </button>
    </div>
  </form>
  <div>
    <div class="m-form-field m-form-field--checkbox reg-checkbox">
      <input class="a-checkbox" type="checkbox" value="1002" id="regulation-1002" name="regs" checked>
      <label class="a-label" for="regulation-1002">
          1002 (Reg<span class="u-hide-on-mobile">ulation</span> B)
      </label>
    </div>
  </div>
  <div class="filters__tags">
    <button class="a-tag-filter" data-value="1002" data-js-hook="behavior_clear-filter">
      <span>1002 (Reg<span class="u-hide-on-mobile">ulation</span> B)</span>
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 718.9 1200" class="cf-icon-svg">
      </svg>
    </button>
  </div>
  <button class="a-btn a-btn--link a-btn--warning filters__clear"
          data-js-hook="behavior_clear-all">
      Clear all filters
  </button>
  <div id="regs3k-results"></div>
`;

global.console = { error: jest.fn(), log: jest.fn() };

/**
 * Create a mock for the window.location object, for testing purposes.
 */
function mockWindowLocation() {
  delete window.location;
  window.location = {
    protocol: 'http:',
    host: 'localhost',
    pathname: '/',
    href: 'http://localhost/',
    assign: jest.fn(),
  };
}

describe('The Regs3K search page', () => {
  beforeEach(() => {
    fetch.resetMocks();
    // Load HTML fixture
    document.body.innerHTML = HTML_SNIPPET;
    // Fire `load` event
    const event = new Event('load', { bubbles: true, cancelable: true });
    window.dispatchEvent(event);
  });

  it('should handle search form submissions', () => {
    mockWindowLocation();
    const form = document.querySelector('form');

    simulateEvent('submit', form);

    expect(global.location.assign).toBeCalledWith(
      'http://localhost/?q=money&regs=1002',
    );
  });

  it('should clear a filter when its X icon is clicked', () => {
    const clearIcon = document.querySelector('.a-tag-filter svg');

    let numFilters = document.querySelectorAll('button.a-tag-filter').length;
    expect(numFilters).toEqual(1);

    simulateEvent('click', clearIcon);
    numFilters = document.querySelectorAll('button.a-tag-filter').length;
    expect(numFilters).toEqual(0);
  });

  it('should clear a filter when its tag is clicked', () => {
    const div = document.querySelector('button.a-tag-filter');

    let numFilters = document.querySelectorAll('button.a-tag-filter').length;
    expect(numFilters).toEqual(1);

    simulateEvent('click', div);
    numFilters = document.querySelectorAll('button.a-tag-filter').length;
    expect(numFilters).toEqual(0);
  });

  it('should clear all filters when the `clear all` link is clicked', () => {
    const clearAllLink = document.querySelector('.filters__clear');

    let numFilters = document.querySelectorAll('button.a-tag-filter').length;
    expect(numFilters).toEqual(1);

    simulateEvent('click', clearAllLink);
    numFilters = document.querySelectorAll('button.a-tag-filter').length;
    expect(numFilters).toEqual(0);
  });

  it('should handle errors when the server is down', (done) => {
    fetch.mockReject(new Error('Server error!'));
    const clearIcon = document.querySelector('.a-tag-filter svg');

    simulateEvent('click', clearIcon);
    setTimeout(() => {
      // eslint-disable-next-line no-console
      expect(console.error).toBeCalled();
      done();
    }, 100);
  });
});
