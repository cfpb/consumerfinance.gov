import { enableFetchMocks } from 'jest-fetch-mock';
const simulateEvent = require('../../../../util/simulate-event').simulateEvent;

import('../../../../../cfgov/unprocessed/apps/regulations3k/js/search.js');

enableFetchMocks();

const HTML_SNIPPET = `
  <form action="/search" data-js-hook="behavior_submit-search">
    <input id="query" name="q" type="text" title="Search terms" class="a-text-input" value="money" placeholder="Search terms">
    <button id="submit">Submit</button>
  </form>
  <div>
    <div class="m-form-field m-form-field__checkbox reg-checkbox">
      <input class="a-checkbox" type="checkbox" value="1002" id="regulation-1002" name="regs" checked>
      <label class="a-label" for="regulation-1002">
          1002 (Regulation B)
      </label>
    </div>
  </div>
  <div class="filters_tags">
    <div class="a-tag" data-value="1002" data-js-hook="behavior_clear-filter">
    1002 (Regulation B)
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 718.9 1200" class="cf-icon-svg">
      </svg>
    </div>
  </div>
  <button class="a-btn a-btn__link a-btn__warning a-micro-copy filters_clear"
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
    const event = document.createEvent('Event');
    event.initEvent('load', true, true);
    window.dispatchEvent(event);
  });

  it('should handle search form submissions', () => {
    mockWindowLocation();
    const form = document.querySelector('form');

    simulateEvent('submit', form);

    expect(global.location.assign).toBeCalledWith(
      'http://localhost/?q=money&regs=1002'
    );
  });

  it('should clear a filter when its X icon is clicked', () => {
    const clearIcon = document.querySelector('svg');

    let numFilters = document.querySelectorAll('div.a-tag').length;
    expect(numFilters).toEqual(1);

    simulateEvent('click', clearIcon);
    numFilters = document.querySelectorAll('div.a-tag').length;
    expect(numFilters).toEqual(0);
  });

  it('should not clear a filter when its tag is clicked', () => {
    const div = document.querySelector('div.a-tag');

    let numFilters = document.querySelectorAll('div.a-tag').length;
    expect(numFilters).toEqual(1);

    simulateEvent('click', div);
    numFilters = document.querySelectorAll('div.a-tag').length;
    expect(numFilters).toEqual(1);
  });

  it('should clear all filters when the `clear all` link is clicked', () => {
    const clearAllLink = document.querySelector('.filters_clear');

    let numFilters = document.querySelectorAll('div.a-tag').length;
    expect(numFilters).toEqual(1);

    simulateEvent('click', clearAllLink);
    numFilters = document.querySelectorAll('div.a-tag').length;
    expect(numFilters).toEqual(0);
  });

  it('should handle errors when the server is down', (done) => {
    fetch.mockReject(new Error('Server error!'));
    const clearIcon = document.querySelector('svg');

    simulateEvent('click', clearIcon);
    setTimeout(() => {
      // eslint-disable-next-line no-console
      expect(console.error).toBeCalled();
      done();
    }, 100);
  });
});
