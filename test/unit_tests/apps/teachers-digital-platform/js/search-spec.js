import { simulateEvent } from '../../../../util/simulate-event.js';

const search = require(
  '../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/search.js'
);

const HTML_SNIPPET = `

  <form class="tdp-activity-search" id="search-form" action="." data-js-hook="behavior_submit-search">
    <div class="input-contains-label">
      <label for="search-text" class="input-contains-label_before input-contains-label_before__search">
          <span class="u-visually-hidden">The term to search for</span>
      </label>
      <input id="search-text" type="text" autocomplete="off" class="a-text-input" name="q" placeholder="Enter your search term(s)" value="executive">
      <label for="search-text" class="input-contains-label_after input-contains-label_after__clear u-hidden">Clear</label>
    </div>
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
  </div>
`;

const xhr = global.XMLHttpRequest;
global.console = { error: jest.fn(), log: jest.fn() };

describe( 'The TDP search page', () => {

  beforeEach( () => {
    // Reset global XHR
    global.XMLHttpRequest = xhr;
    // Load HTML fixture
    document.body.innerHTML = HTML_SNIPPET;
    // Fire init
    search.init();
  } );

  it( 'should not throw any errors on init', () => {
    expect( () => search.init() ).not.toThrow();
  } );

  it( 'should handle search form submissions', () => {
    const mockXHR = {
      open: jest.fn(),
      send: jest.fn(),
      readyState: 4,
      status: 200,
      onreadystatechange: jest.fn(),
      responseText: []
    };
    global.XMLHttpRequest = jest.fn( () => mockXHR );
    const form = document.querySelector( 'form#search-form' );
    simulateEvent( 'submit', form );
    expect( window.location.href ).toEqual( 'http://localhost/?q=executive' );
  } );

  it( 'should clear a filter when its X icon is clicked', () => {
    const mockXHR = {
      open: jest.fn(),
      send: jest.fn(),
      readyState: 4,
      status: 200,
      onreadystatechange: jest.fn(),
      responseText: []
    };
    global.XMLHttpRequest = jest.fn( () => mockXHR );
    const clearIcon = document.querySelector( '.results_filters svg' );

    let numFilters = document.querySelectorAll( 'div.a-tag' ).length;
    expect( numFilters ).toEqual( 2 );

    simulateEvent( 'click', clearIcon );
    numFilters = document.querySelectorAll( 'div.a-tag' ).length;
    expect( numFilters ).toEqual( 1 );

    mockXHR.onreadystatechange();
  } );

  it( 'should not clear a filter when its tag is clicked', () => {
    const div = document.querySelector( 'div.a-tag' );

    let numFilters = document.querySelectorAll( 'div.a-tag' ).length;
    expect( numFilters ).toEqual( 2 );

    simulateEvent( 'click', div );
    numFilters = document.querySelectorAll( 'div.a-tag' ).length;
    expect( numFilters ).toEqual( 2 );
  } );

  it( 'should clear all filters when the `clear all` link is clicked', () => {
    const mockXHR = {
      open: jest.fn(),
      send: jest.fn(),
      readyState: 4,
      status: 200,
      onreadystatechange: jest.fn(),
      responseText: []
    };
    global.XMLHttpRequest = jest.fn( () => mockXHR );
    const clearAllLink = document.querySelector( '.results_filters-clear' );

    let numFilters = document.querySelectorAll( 'div.a-tag' ).length;
    expect( numFilters ).toEqual( 2 );

    simulateEvent( 'click', clearAllLink );
    numFilters = document.querySelectorAll( 'div.a-tag' ).length;
    expect( numFilters ).toEqual( 0 );

    mockXHR.onreadystatechange();
  } );

  it( 'should check nested filter when parent filter is clicked', () => {
    const mockXHR = {
      open: jest.fn(),
      send: jest.fn(),
      readyState: 4,
      status: 200,
      onreadystatechange: jest.fn(),
      responseText: []
    };
    global.XMLHttpRequest = jest.fn( () => mockXHR );
    const parentCheckbox = document.querySelector( '#topic--earn' );

    let numChecked = document.querySelectorAll(
      '.o-expandable-facets .a-checkbox:checked'
    ).length;
    expect( numChecked ).toEqual( 1 );

    parentCheckbox.checked = true;
    simulateEvent( 'change', parentCheckbox );
    numChecked = document.querySelectorAll(
      '.o-expandable-facets .a-checkbox:checked'
    ).length;
    expect( numChecked ).toEqual( 3 );
    expect(
      window.location.href
    ).toEqual(
      'http://localhost/?q=executive&building_block=1&topic=1&topic=4&topic=2'
    );

    const childCheckbox = document.querySelector( '#topic--getting-paid' );
    childCheckbox.checked = false;
    simulateEvent( 'change', childCheckbox );
    numChecked = document.querySelectorAll(
      '.o-expandable-facets .a-checkbox:checked'
    ).length;
    expect( numChecked ).toEqual( 1 );
    expect(
      window.location.href
    ).toEqual(
      'http://localhost/?q=executive&building_block=1&topic=2'
    );

  } );

  it( 'should handle errors when the server is down', done => {
    const mockXHR = {
      open: jest.fn(),
      send: jest.fn(),
      readyState: 4,
      status: 404,
      onreadystatechange: jest.fn(),
      responseText: 'Server error!'
    };
    global.XMLHttpRequest = jest.fn( () => mockXHR );
    const clearIcon = document.querySelector( '.results_filters svg' );

    simulateEvent( 'click', clearIcon );
    setTimeout( () => {
      // eslint-disable-next-line no-console
      expect( console.error ).toBeCalled();
      done();
    }, 100 );

    mockXHR.onreadystatechange();
  } );

} );
