import { simulateEvent } from '../../../../util/simulate-event';
const BASE_JS_PATH = '../../../../../cfgov/unprocessed/apps/';
const tdpAnalytics = require(
  BASE_JS_PATH + 'teachers-digital-platform/js/tdp-analytics.js'
);

const HTML_SNIPPET = `

  <form id="search-form" action="." data-js-hook="behavior_submit-search">
    <input id="search-text" type="text" autocomplete="off" class="a-text-input" name="q" placeholder="Enter your search term(s)" value="executive">
    <button class="a-btn">Search</button>
  </form>


  <div id="tdp-search-facets-and-results" style="opacity: 1;">

    <form id="filter-form" action="." method="get" data-js-hook="behavior_change-filter">
      <input type="hidden" name="q" value="{% if search_query: %}{{ search_query }}{% endif %}">
      <input type="hidden" name="page" inputmode="numeric" value="1">
      <div data-qa-hook="expandable" class="o-expandable o-expandable__padded o-expandable__background" data-bound="true">
        <button class="o-expandable_header o-expandable_target o-expandable_target__expanded" type="button">
          <span class="h4 o-expandable_header-left o-expandable_label">
            Building block
          </span>
          <span class="o-expandable_header-right o-expandable_link">
            <span class="o-expandable_cue o-expandable_cue-open">
              <span class="u-visually-hidden-on-mobile u-visually-hidden">Show</span>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1200" class="cf-icon-svg"><path d="M500 105.2c-276.1 0-500 223.9-500 500s223.9 500 500 500 500-223.9 500-500-223.9-500-500-500zm263.1 550.7H549.6v213.6c0 27.6-22.4 50-50 50s-50-22.4-50-50V655.9H236c-27.6 0-50-22.4-50-50s22.4-50 50-50h213.6V342.3c0-27.6 22.4-50 50-50s50 22.4 50 50v213.6h213.6c27.6 0 50 22.4 50 50s-22.5 50-50.1 50z"></path></svg>
            </span>
            <span class="o-expandable_cue o-expandable_cue-close">
              <span class="u-visually-hidden-on-mobile u-visually-hidden">Hide</span>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1200" class="cf-icon-svg"><path d="M500 105.2c-276.1 0-500 223.9-500 500s223.9 500 500 500 500-223.9 500-500-223.9-500-500-500zm263.1 550.7H236c-27.6 0-50-22.4-50-50s22.4-50 50-50h527.1c27.6 0 50 22.4 50 50s-22.4 50-50 50z"></path></svg>
            </span>
          </span>
        </button>
        <div class="o-expandable_content o-expandable_content__transition o-expandable_content__expanded" style="max-height: 119px;">
          <div class="o-form_group u-mt15">
            <fieldset class="o-form_fieldset">
              <ul class="m-list m-list__unstyled">
                <li>
                  <div class="m-form-field m-form-field__checkbox">
                    <input type="checkbox" class="a-checkbox" aria-label="Executive function" id="building-block--executive-function" name="building_block" value="1" checked="checked">
                    <label class="a-label" for="building-block--executive-function">Executive function</label>
                  </div>
                </li>
                <li>
                  <div class="m-form-field m-form-field__checkbox">
                    <input type="checkbox" class="a-checkbox" aria-label="Financial habits and norms" id="building-block--financial-habits-and-norms" name="building_block" value="2">
                    <label class="a-label" for="building-block--financial-habits-and-norms">Financial habits and norms</label>
                  </div>
                </li>
                <li>
                  <div class="m-form-field m-form-field__checkbox">
                    <input type="checkbox" class="a-checkbox" aria-label="Financial knowledge and decision-making skills" id="building-block--financial-knowledge-and-decision-making-skills" name="building_block" value="3">
                    <label class="a-label" for="building-block--financial-knowledge-and-decision-making-skills">Financial knowledge and decision-making skills</label>
                  </div>
                </li>
              </ul>
            </fieldset>
          </div>
        </div>
      </div>

      <div data-qa-hook="expandable" class="o-expandable o-expandable__padded o-expandable__background" data-bound="true">
        <button class="o-expandable_header o-expandable_target o-expandable_target__expanded" type="button">
          <span class="h4 o-expandable_header-left o-expandable_label">Topic</span>
          <span class="o-expandable_header-right o-expandable_link">
            <span class="o-expandable_cue o-expandable_cue-open">Show</span>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1200" class="cf-icon-svg"><path d="M500 105.2c-276.1 0-500 223.9-500 500s223.9 500 500 500 500-223.9 500-500-223.9-500-500-500zm263.1 550.7H549.6v213.6c0 27.6-22.4 50-50 50s-50-22.4-50-50V655.9H236c-27.6 0-50-22.4-50-50s22.4-50 50-50h213.6V342.3c0-27.6 22.4-50 50-50s50 22.4 50 50v213.6h213.6c27.6 0 50 22.4 50 50s-22.5 50-50.1 50z"></path></svg>
            </span>
            <span class="o-expandable_cue o-expandable_cue-close">
              <span class="u-visually-hidden-on-mobile u-visually-hidden">Hide</span>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1200" class="cf-icon-svg"><path d="M500 105.2c-276.1 0-500 223.9-500 500s223.9 500 500 500 500-223.9 500-500-223.9-500-500-500zm263.1 550.7H236c-27.6 0-50-22.4-50-50s22.4-50 50-50h527.1c27.6 0 50 22.4 50 50s-22.4 50-50 50z"></path></svg>
            </span>
          </span>
        </button>
        <div class="o-expandable_content o-expandable_content__transition o-expandable_content__expanded" style="max-height: 337px;">
          <ul class="m-list m-list__unstyled u-mt15">
            <li class="o-expandable-facets" data-bound="true">
              <div class="m-form-field m-form-field__checkbox">
                <input type="checkbox" class="a-checkbox o-expandable-facets_checkbox" aria-label="Earn" id="topic--earn" name="topic" value="1">
                <label class="a-label toggle indeterminate" for="topic--earn">
                  <span class="u-visually-hidden">Earn</span>
                  <span class="u-hide-on-med u-hide-on-lg u-hide-on-xl" aria-hidden="true">Earn</span>
                </label>
                <button class="a-btn a-btn__link u-hide-on-xs u-hide-on-sm o-expandable-facets_target is-open" type="button">
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
              <ul class="m-list m-list__unstyled o-expandable-facets_content o-expandable-facets_content__transition o-expandable-facets_content__expanded" style="max-height: 52px;">
                <li class="u-hide-on-xs u-hide-on-sm">
                  <div class="m-form-field m-form-field__checkbox">
                    <input type="checkbox" class="a-checkbox" aria-label="Getting paid" id="topic--getting-paid" name="topic" value="4" checked="checked">
                    <label class="a-label" for="topic--getting-paid">Getting paid</label>
                  </div>
                </li>
                <li class="u-hide-on-xs u-hide-on-sm">
                  <div class="m-form-field m-form-field__checkbox">
                    <input type="checkbox" class="a-checkbox" aria-label="Making money" id="topic--making-money" name="topic" value="2">
                    <label class="a-label" for="topic--making-money">Making money</label>
                  </div>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>



      <div id="tdp-search-results">
        <div class="results_header">
          <div class="results_count" data-results-count="8">
            <h3>Showing 8 matches out of 26 activities</h3>
          </div>
          <div class="results_filters">
            <span class="results_filters-label">Filters applied</span>
            <div class="results_filters-tags">
              <div class="a-tag" data-value="#building-block--executive-function" data-js-hook="behavior_clear-filter">
                Executive function
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 718.9 1200" class="cf-icon-svg"><path d="M451.4 613.7l248.1-248.1c25.6-25.1 26-66.3.8-91.9s-66.3-26-91.9-.8l-.8.8-248.1 248.1-248.1-248.1c-25.4-25.4-66.5-25.4-91.9 0s-25.4 66.5 0 91.9l248.1 248.1L19.5 861.8c-25.6 25.1-26 66.3-.8 91.9s66.3 26 91.9.8l.8-.8 248.1-248.1 248.1 248.1c25.4 25.4 66.5 25.4 91.9 0s25.4-66.5 0-91.9L451.4 613.7z"></path></svg>
              </div>
              <div class="a-tag" data-value="#topic--getting-paid" data-js-hook="behavior_clear-filter">
                Getting paid
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 718.9 1200" class="cf-icon-svg"><path d="M451.4 613.7l248.1-248.1c25.6-25.1 26-66.3.8-91.9s-66.3-26-91.9-.8l-.8.8-248.1 248.1-248.1-248.1c-25.4-25.4-66.5-25.4-91.9 0s-25.4 66.5 0 91.9l248.1 248.1L19.5 861.8c-25.6 25.1-26 66.3-.8 91.9s66.3 26 91.9.8l.8-.8 248.1-248.1 248.1 248.1c25.4 25.4 66.5 25.4 91.9 0s25.4-66.5 0-91.9L451.4 613.7z"></path></svg>
              </div>
              <button class="a-btn a-btn__link a-btn__warning a-micro-copy results_filters-clear u-mb10" data-js-hook="behavior_clear-all">Clear all filters</button>
            </div>
          </div>
        </div>
        <div class="results_list"></div>
      </div>

    </form>
    <nav class="m-pagination" role="navigation" aria-label="Pagination">
        <a class="a-btn
                  m-pagination_btn-prev"
           href="?page=21#pagination_content">
            <span class="a-btn_icon a-btn_icon__on-left">{% include icons/left.svg %}</span>
            Newer
        </a>
        <a class="a-btn
                  m-pagination_btn-next"
           href="?page=23#pagination_content">
            <span class="a-btn_icon a-btn_icon__on-right">{% include icons/right.svg %}</span>
            Older
        </a>
        <form class="m-pagination_form"
              action="#pagination_content">
            <label class="m-pagination_label"
                   for="m-pagination_current-page">
                Page
                <span class="u-visually-hidden">
                    number 22 out
                </span>
                <input class="m-pagination_current-page"
                       id="m-pagination_current-page"
                       name="page"
                       type="number"
                       min="1"
                       max="149"
                       pattern="[0-9]*"
                       inputmode="numeric"
                       value="22">
                of 149
            </label>
            <button class="a-btn
                           a-btn__link
                           m-pagination_btn-submit"
                    id="m-pagination_btn-submit"
                    type="submit">Go</button>
        </form>
    </nav>
  </div>
`;

const xhr = global.XMLHttpRequest;

describe( 'The TDP custom analytics', () => {

  beforeEach( () => {
    // Reset global XHR
    global.XMLHttpRequest = xhr;
    // Load HTML fixture
    document.body.innerHTML = HTML_SNIPPET;
    // Fire `load` event
    const event = document.createEvent( 'Event' );
    event.initEvent( 'load', true, true );
    window.dispatchEvent( event );

    const mockXHR = {
      open: jest.fn(),
      send: jest.fn(),
      readyState: 4,
      status: 200,
      onreadystatechange: jest.fn(),
      responseText: []
    };
    global.XMLHttpRequest = jest.fn( () => mockXHR );
  } );

  it( 'should not throw any errors on bind', () => {
    expect( () => tdpAnalytics.bindAnalytics() ).not.toThrow();
  } );


  it( 'should send an analytics event when a filter clear icon is clicked', () => {
    const clearIcon = document.querySelector( '.results_filters svg' );
    const spy = jest.fn();

    tdpAnalytics.bindAnalytics( spy );

    simulateEvent( 'click', clearIcon );

    expect( spy ).toHaveBeenCalled();
  } );

  it( 'should NOT send an analytics event when a filter is clicked (but not its clear icon)', () => {
    const filterTag = document.querySelector( '.results_filters .a-tag' );
    const spy = jest.fn();

    tdpAnalytics.bindAnalytics( spy );

    simulateEvent( 'click', filterTag );

    expect( spy ).not.toHaveBeenCalled();
  } );

  it( 'should send an analytics event when a pagination button is clicked', () => {
    const paginationButton = document.querySelector( '.m-pagination_btn-next' );
    const spy = jest.fn();

    tdpAnalytics.bindAnalytics( spy );

    simulateEvent( 'click', paginationButton );

    expect( spy ).toHaveBeenCalled();
  } );

  it( 'should send an analytics event when an expandable is clicked', () => {
    const expandable = document.querySelector( '.o-expandable_header' );
    const spy = jest.fn();

    tdpAnalytics.bindAnalytics( spy );

    simulateEvent( 'click', expandable );

    expect( spy ).toHaveBeenCalled();
  } );

} );
