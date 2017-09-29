'use strict';

const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';
const chai = require( 'chai' );
const expect = chai.expect;
const jsdom = require( 'mocha-jsdom' );
const sinon = require( 'sinon' );
let expandableContent;
let expandableTarget;
let fwbResults;
let sandbox;
let toggleButtons;
const dataLayerEvent = {
  event: 'Financial Well-Being Tool Interaction',
  action: 'Compare By Button Clicked',
  label: 'Age',
  eventCallback: undefined, // eslint-disable-line  no-undefined
  eventTimeout: 500
};

const HTML_SNIPPET =
`<div class="content">
  <div class="o-expandable">
    <button class="o-expandable_target">
        <div class="o-expandable_header">
          <span class="o-expandable_header-left o-expandable_label">
          </span>
          <span class="o-expandable_header-right o-expandable_link">
              <span class="o-expandable_cue o-expandable_cue-open">
                  <span class="cf-icon cf-icon-plus-round"></span>
              </span>
              <span class="o-expandable_cue o-expandable_cue-close">
                  <span class="cf-icon cf-icon-minus-round"></span>
              </span>
          </span>
      </div>
    </button>
    <div class="o-expandable_content">
        <div class="o-expandable_content-animated">
        </div>
    </div>
  </div>
  <figure class="comparison-chart" id="comparison-chart">
    <div class="comparison-chart_toggle u-js-only">
        <h4>Compare by</h4>
        <button class="a-btn comparison-chart_toggle-button comparison-chart_toggle-button__selected"
               data-compare-by="age"
               data-gtm-action="Compare By Button Clicked"
               data-gtm-label="Age"
               data-gtm-category="Financial Well-Being Tool Interaction">
            Age
        </button>
        <button class="a-btn comparison-chart_toggle-button"
                data-compare-by="income"
                data-gtm-action="Compare By Button Clicked"
                data-gtm-label="Household income"
                data-gtm-category="Financial Well-Being Tool Interaction">
            Household income
        </button>
        <button class="a-btn comparison-chart_toggle-button"
                data-compare-by="employment"
                data-gtm-action="Compare By Button Clicked"
                data-gtm-label="Employment status"
                data-gtm-category="Financial Well-Being Tool Interaction">
            Employment status
        </button>
    </div>
    <dl class="comparison-chart_list">
        <dt><b>Your score</b></dt>
        <dd>
            <span style="left: 48.1481481481%; border-color: #a6a329;">
                53
            </span>
        </dd>
        <dt>U.S. average</dt>
    </dl>
  </figure>
</div>`;

function triggerClickEvent( target ) {
  var event = document.createEvent( 'Event' );
  event.initEvent( 'click', true, true );
  return target.dispatchEvent( event );
}

function initFwbResults( ) {
  fwbResults = require( BASE_JS_PATH + 'apps/financial-well-being/fwb-results' );
  fwbResults.init();
}

describe( 'fwb-results', () => {
  jsdom();

  beforeEach( () => {
    sandbox = sinon.sandbox.create();
    document.body.innerHTML = HTML_SNIPPET;
    window.dataLayer = [];
    window.tagManagerIsLoaded = true;
    Object.defineProperty(window.location, 'pathname', {
      value: 'http://example.com/results'
    } );

    toggleButtons = document.querySelectorAll(
      '.comparison-chart_toggle-button'
    );
    expandableContent = document.querySelector( '.o-expandable_content' );
    expandableTarget = document.querySelector( '.o-expandable_target' );
  } );

  afterEach( () => {
    sandbox.restore();
  } );

  it( 'initialize the expandables on page load', () => {
    initFwbResults();
    expect( expandableTarget.getAttribute( 'aria-pressed' ) )
    .to.equal( 'false' );

    expect( expandableContent.getAttribute( 'aria-expanded' ) )
    .to.equal( 'false' );
  } );

  it( 'should submit the correct analytics when a toggle button is clicked',
    () => {
      initFwbResults();
      triggerClickEvent( toggleButtons[0] );
      expect( window.dataLayer[0] ).to.deep.equal( dataLayerEvent );
    }
  );

} );
