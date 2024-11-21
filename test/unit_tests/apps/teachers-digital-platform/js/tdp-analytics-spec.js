import { jest } from '@jest/globals';
import { simulateEvent } from '../../../../util/simulate-event.js';
import {
  bindAnalytics,
  handleFetchSearchResults,
} from '../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/tdp-analytics.js';

const EMPTY_SEARCH_HTML = `
  <div id="tdp-search-facets-and-results">
    <div class="results__count" data-results-count="0">
    </div>
  </div>
`;

const HTML_SNIPPET = `
  <form id="search-form" action="." data-js-hook="behavior_submit-search">
    <input id="search-text" type="text" autocomplete="off" class="a-text-input" name="q" placeholder="Enter your search term(s)" value="executive">
    <button class="a-btn">Search</button>
  </form>

  <div id="tdp-search-facets-and-results" style="opacity: 1;">

    <form id="filter-form" action="." method="get" data-js-hook="behavior_change-filter">
      <input type="hidden" name="q" value="{% if search_query: %}{{ search_query }}{% endif %}">
      <input type="hidden" name="page" inputmode="numeric" value="1">
      <div class="o-expandable o-expandable--background" data-bound="true">
        <button class="o-expandable__header o-expandable__target--expanded" type="button">
          <span class="o-expandable__label">
            Building block
          </span>
          <span class="o-expandable__cues">
            <span class="o-expandable__cue-open" role="img" aria-label="Show">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1200" class="cf-icon-svg"><path d="M500 105.2c-276.1 0-500 223.9-500 500s223.9 500 500 500 500-223.9 500-500-223.9-500-500-500zm263.1 550.7H549.6v213.6c0 27.6-22.4 50-50 50s-50-22.4-50-50V655.9H236c-27.6 0-50-22.4-50-50s22.4-50 50-50h213.6V342.3c0-27.6 22.4-50 50-50s50 22.4 50 50v213.6h213.6c27.6 0 50 22.4 50 50s-22.5 50-50.1 50z"></path></svg>
            </span>
            <span class="o-expandable__cue-close" role="img" aria-label="Hide">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1200" class="cf-icon-svg"><path d="M500 105.2c-276.1 0-500 223.9-500 500s223.9 500 500 500 500-223.9 500-500-223.9-500-500-500zm263.1 550.7H236c-27.6 0-50-22.4-50-50s22.4-50 50-50h527.1c27.6 0 50 22.4 50 50s-22.4 50-50 50z"></path></svg>
            </span>
          </span>
        </button>
        <div class="o-expandable__content o-expandable__content--transition o-expandable__content--expanded" style="max-height: 119px;">
          <div class="o-form__group u-mt15">
            <fieldset class="o-form__fieldset">
              <ul class="m-list m-list--unstyled">
                <li>
                  <div class="m-form-field m-form-field--checkbox">
                    <input type="checkbox" class="a-checkbox" aria-label="Executive function" id="building-block--executive-function" name="building_block" value="1" checked="checked">
                    <label class="a-label" for="building-block--executive-function">Executive function</label>
                  </div>
                </li>
                <li>
                  <div class="m-form-field m-form-field--checkbox">
                    <input type="checkbox" class="a-checkbox" aria-label="Financial habits and norms" id="building-block--financial-habits-and-norms" name="building_block" value="2">
                    <label class="a-label" for="building-block--financial-habits-and-norms">Financial habits and norms</label>
                  </div>
                </li>
                <li>
                  <div class="m-form-field m-form-field--checkbox">
                    <input type="checkbox" class="a-checkbox" aria-label="Financial knowledge and decision-making skills" id="building-block--financial-knowledge-and-decision-making-skills" name="building_block" value="3">
                    <label class="a-label" for="building-block--financial-knowledge-and-decision-making-skills">Financial knowledge and decision-making skills</label>
                  </div>
                </li>
              </ul>
            </fieldset>
          </div>
        </div>
      </div>

      <div class="o-expandable o-expandable--background" data-bound="true">
        <button class="o-expandable__header o-expandable__target--expanded" type="button">
          <span class="o-expandable__label">Topic</span>
          <span class="o-expandable__cues">
            <span class="o-expandable__cue-open" role="img" aria-label="Show">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1200" class="cf-icon-svg"><path d="M500 105.2c-276.1 0-500 223.9-500 500s223.9 500 500 500 500-223.9 500-500-223.9-500-500-500zm263.1 550.7H549.6v213.6c0 27.6-22.4 50-50 50s-50-22.4-50-50V655.9H236c-27.6 0-50-22.4-50-50s22.4-50 50-50h213.6V342.3c0-27.6 22.4-50 50-50s50 22.4 50 50v213.6h213.6c27.6 0 50 22.4 50 50s-22.5 50-50.1 50z"></path></svg>
            </span>
            <span class="o-expandable__cue-close" role="img" aria-label="Hide">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1200" class="cf-icon-svg"><path d="M500 105.2c-276.1 0-500 223.9-500 500s223.9 500 500 500 500-223.9 500-500-223.9-500-500-500zm263.1 550.7H236c-27.6 0-50-22.4-50-50s22.4-50 50-50h527.1c27.6 0 50 22.4 50 50s-22.4 50-50 50z"></path></svg>
            </span>
          </span>
        </button>
        <div class="o-expandable__content o-expandable__content--transition o-expandable__content--expanded" style="max-height: 337px;">
          <ul class="m-list m-list--unstyled u-mt15">
            <li class="o-expandable-facets" data-bound="true">
              <div class="m-form-field m-form-field--checkbox">
                <input type="checkbox" class="a-checkbox o-expandable-facets__checkbox" aria-label="Earn" id="topic-earn" name="topic" value="1">
                <label class="a-label toggle indeterminate" for="topic-earn">
                  <span class="u-visually-hidden">Earn</span>
                  <span class="u-hide-on-med u-hide-on-lg u-hide-on-xl" aria-hidden="true">Earn</span>
                </label>
                <button class="a-btn a-btn--link u-hide-on-xs u-hide-on-sm o-expandable-facets__target is-open" type="button">
                  <span class="u-visually-hidden">Expand children</span>
                  <span aria-hidden="true">Earn</span>
                  <span class="o-expandable-facets_cue o-expandable-facets_cue-open">
                    <span class="u-visually-hidden">Show</span>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 988.2 1200" class="cf-icon-svg"><path d="M494.1 967.2c-17.3 0-33.8-6.8-46-19L18.6 518.6c-25.1-25.6-24.8-66.8.8-91.9 25.3-24.8 65.8-24.8 91.1 0l383.6 383.6 383.6-383.6c25.6-25.1 66.8-24.8 91.9.8 24.8 25.3 24.8 65.8 0 91.1L540.1 948.1c-12.2 12.2-28.7 19.1-46 19.1z"></path></svg>
                  </span>
                  <span class="o-expandable-facets_cue o-expandable-facets_cue-close">
                    <span class="u-visually-hidden">Hide</span>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 988.7 1200" class="cf-icon-svg"><path d="M923.6 967.6c-17.3 0-33.8-6.8-46-19L494.1 565 110.5 948.5c-25.6 25.1-66.8 24.8-91.9-.8-24.8-25.3-24.8-65.8 0-91.1l429.5-429.5c25.4-25.4 66.5-25.4 91.9 0l429.6 429.5c25.4 25.4 25.4 66.5.1 91.9-12.3 12.3-28.8 19.1-46.1 19.1z"></path></svg>
                  </span>
                </button>
              </div>
              <ul class="m-list m-list--unstyled o-expandable-facets__content o-expandable-facets__content--transition o-expandable-facets__content--expanded" style="max-height: 52px;">
                <li class="u-hide-on-xs u-hide-on-sm">
                  <div class="m-form-field m-form-field--checkbox">
                    <input type="checkbox" class="a-checkbox" aria-label="Getting paid" id="topic-getting-paid" name="topic" value="4" checked="checked">
                    <label class="a-label" for="topic-getting-paid">Getting paid</label>
                  </div>
                </li>
                <li class="u-hide-on-xs u-hide-on-sm">
                  <div class="m-form-field m-form-field--checkbox">
                    <input type="checkbox" class="a-checkbox" aria-label="Making money" id="topic-making-money" name="topic" value="2">
                    <label class="a-label" for="topic-making-money">Making money</label>
                  </div>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>



      <div id="tdp-search-results">
        <div class="results__header">
          <div class="results__count" data-results-count="8">
            <h3>Showing 8 matches out of 26 activities</h3>
          </div>
          <div class="results__filters">
            <span class="results__filters-label">Filters applied</span>
            <div class="results__filters-tags">
              <button class="a-tag-filter" data-value="#building-block--executive-function" data-js-hook="behavior_clear-filter">
                Executive function
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 718.9 1200" class="cf-icon-svg"><path d="M451.4 613.7l248.1-248.1c25.6-25.1 26-66.3.8-91.9s-66.3-26-91.9-.8l-.8.8-248.1 248.1-248.1-248.1c-25.4-25.4-66.5-25.4-91.9 0s-25.4 66.5 0 91.9l248.1 248.1L19.5 861.8c-25.6 25.1-26 66.3-.8 91.9s66.3 26 91.9.8l.8-.8 248.1-248.1 248.1 248.1c25.4 25.4 66.5 25.4 91.9 0s25.4-66.5 0-91.9L451.4 613.7z"></path></svg>
              </button>
              <button class="a-tag-filter" data-value="#topic-getting-paid" data-js-hook="behavior_clear-filter">
                Getting paid
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 718.9 1200" class="cf-icon-svg"><path d="M451.4 613.7l248.1-248.1c25.6-25.1 26-66.3.8-91.9s-66.3-26-91.9-.8l-.8.8-248.1 248.1-248.1-248.1c-25.4-25.4-66.5-25.4-91.9 0s-25.4 66.5 0 91.9l248.1 248.1L19.5 861.8c-25.6 25.1-26 66.3-.8 91.9s66.3 26 91.9.8l.8-.8 248.1-248.1 248.1 248.1c25.4 25.4 66.5 25.4 91.9 0s25.4-66.5 0-91.9L451.4 613.7z"></path></svg>
              </button>
              <button class="a-btn a-btn--link a-btn--warning results__filters-clear u-mb10" data-js-hook="behavior_clear-all">Clear all filters</button>
            </div>
          </div>
        </div>
        <div class="results__list"></div>
      </div>

    </form>
    <nav class="m-pagination" role="navigation" aria-label="Pagination">
        <a class="a-btn m-pagination__btn-prev"
           href="?page=21#pagination_content">
            {% include icons/left.svg %}
            <span>Previous</span>
        </a>
        <form class="m-pagination__form"
              action="#pagination_content">
            <label class="m-pagination__label">
                Page
                <span class="u-visually-hidden">
                    number 22 out
                </span>
                <input class="m-pagination__current-page"
                       id="m-pagination__current-page"
                       name="page"
                       type="number"
                       min="1"
                       max="149"
                       pattern="[0-9]*"
                       inputmode="numeric"
                       value="22">
                <span class="m-pagination__label"> of 149</span>
            </label>
            <button class="a-btn
                           a-btn--link
                           m-pagination__btn-submit"
                    id="m-pagination__btn-submit"
                    type="submit">Go</button>
        </form>
        <a class="a-btn m-pagination__btn-next"
           href="?page=23#pagination_content">
            <span>Next</span>
            {% include icons/right.svg %}
        </a>
    </nav>
  </div>
`;

const xhr = global.XMLHttpRequest;

describe('The TDP custom analytics', () => {
  beforeEach(() => {
    // Reset global XHR
    global.XMLHttpRequest = xhr;
    // Load HTML fixture
    document.body.innerHTML = HTML_SNIPPET;
    // Fire `load` event
    const event = new Event('load', { bubbles: true, cancelable: true });
    window.dispatchEvent(event);

    const mockXHR = {
      open: jest.fn(),
      send: jest.fn(),
      readyState: 4,
      status: 200,
      onreadystatechange: jest.fn(),
      responseText: [],
    };
    global.XMLHttpRequest = jest.fn(() => mockXHR);
  });

  it('should not throw any errors on bind', () => {
    expect(() => bindAnalytics()).not.toThrow();
  });

  it('should send an analytics event when a filter is clicked', () => {
    const filterTag = document.querySelector('.results__filters .a-tag-filter');
    const spy = jest.fn();

    bindAnalytics(spy);

    simulateEvent('click', filterTag);

    expect(spy).toHaveBeenCalled();
  });

  it('should send an analytics event when next pagination button is clicked', () => {
    const paginationButton = document.querySelector('.m-pagination__btn-next');
    const spy = jest.fn();

    bindAnalytics(spy);

    simulateEvent('click', paginationButton);

    expect(spy).toHaveBeenCalled();
  });

  it('should send an analytics event when an expandable is clicked', () => {
    const expandable = document.querySelector('.o-expandable__header');
    const spy = jest.fn();

    bindAnalytics(spy);

    simulateEvent('click', expandable);

    expect(spy).toHaveBeenCalled();
  });

  it('should send an analytics event when no search results are found', () => {
    document.body.innerHTML = EMPTY_SEARCH_HTML;
    const spy = jest.fn();

    bindAnalytics(spy);

    handleFetchSearchResults('Not Found');

    expect(JSON.stringify(spy.mock.calls[0][0])).toEqual(
      '{"event":"TDP Search Tool","action":"noSearchResults","label":"not found:0"}',
    );
  });
});
