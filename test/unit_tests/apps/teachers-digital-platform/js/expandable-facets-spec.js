import { simulateEvent } from '../../../../util/simulate-event';
import ExpandableFacets from '../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/expandable-facets.js';

let ef;
// let efLabel;
let efTarget;
// let efHeader;
let efBody;
let expandableFacet;

const HTML_SNIPPET = `
  <ul class="m-list m-list__unstyled u-mt15">
    <li class="o-expandable-facets" data-bound="true">
      <div class="m-form-field m-form-field__checkbox">
        <input type="checkbox" class="a-checkbox o-expandable-facets_checkbox" aria-label="Earn" id="topic--earn" name="topic" value="1">
        <label class="a-label toggle" for="topic--earn">
          <span class="u-visually-hidden">Earn</span>
          <span class="u-hide-on-med u-hide-on-lg u-hide-on-xl" aria-hidden="true">Earn</span>
        </label>
        <button class="a-btn a-btn__link u-hide-on-xs u-hide-on-sm o-expandable-facets_target" type="button">
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
      <ul class="m-list m-list__unstyled o-expandable-facets_content o-expandable-facets_content__transition" style="max-height: 52px;">
        <li class="u-hide-on-xs u-hide-on-sm">
          <div class="m-form-field m-form-field__checkbox">
            <input type="checkbox" class="a-checkbox" aria-label="Getting paid" id="topic--getting-paid" name="topic" value="4">
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
`;

const xhr = global.XMLHttpRequest;
global.console = { error: jest.fn(), log: jest.fn() };

describe( 'Expandable facets', () => {

  beforeEach( () => {
    // Reset global XHR
    global.XMLHttpRequest = xhr;
    // Load HTML fixture
    document.body.innerHTML = HTML_SNIPPET;
    // Fire `load` event
    const event = document.createEvent( 'Event' );
    event.initEvent( 'load', true, true );
    window.dispatchEvent( event );

    ef = document.querySelector( '.o-expandable-facets' );
    expandableFacet = new ExpandableFacets( ef );
    expandableFacet.init();
    // efLabel = document.querySelector( '.o-expandable-facets_checkbox ~ .a-label' );
    efTarget = document.querySelector( '.o-expandable-facets_target' );
    // efHeader = document.querySelector( '.o-expandable_header' );
    efBody = document.querySelector( '.o-expandable-facets_content' );

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

  it( 'should not throw any errors on init', () => {
    expect( () => ExpandableFacets.init() ).not.toThrow();
  } );

  it( 'should collapse an expanded facet when label is clicked', () => {

    expect( efTarget.classList.contains( 'is-open' ) ).toEqual( false );
    expect( efTarget.classList.contains( 'is-closed' ) ).toEqual( true );
    expect( efBody.classList.contains( 'o-expandable-facets_content__expanded' ) ).toEqual( false );
    expect( efBody.classList.contains( 'o-expandable-facets_content__collapsed' ) ).toEqual( true );

    simulateEvent( 'click', efTarget );

    expect( efTarget.classList.contains( 'is-closed' ) ).toEqual( false );
    expect( efTarget.classList.contains( 'is-open' ) ).toEqual( true );
    expect( efBody.classList.contains( 'o-expandable-facets_content__expanded' ) ).toEqual( true );
    expect( efBody.classList.contains( 'o-expandable-facets_content__collapsed' ) ).toEqual( false );

  } );

  it( 'should expand a collapsed facet when label is clicked', () => {

    expect( efTarget.classList.contains( 'is-open' ) ).toEqual( false );
    expect( efTarget.classList.contains( 'is-closed' ) ).toEqual( true );

    simulateEvent( 'click', efTarget );

    expect( efTarget.classList.contains( 'is-closed' ) ).toEqual( false );
    expect( efTarget.classList.contains( 'is-open' ) ).toEqual( true );

    simulateEvent( 'click', efTarget );

    expect( efTarget.classList.contains( 'is-closed' ) ).toEqual( true );
    expect( efTarget.classList.contains( 'is-open' ) ).toEqual( false );
    expect( efBody.classList.contains( 'o-expandable-facets_content__expanded' ) ).toEqual( false );
    expect( efBody.classList.contains( 'o-expandable-facets_content__collapsed' ) ).toEqual( true );

  } );

} );
