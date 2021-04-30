import fwbResults from '../../../../../cfgov/unprocessed/apps/financial-well-being/js/fwb-results.js';
import { simulateEvent } from '../../../../util/simulate-event.js';

const SELECTED_CLASS = 'comparison-chart_toggle-button__selected';
const HIDDEN_CLASS = 'u-hidden';

let expandableContent;
let expandableTarget;
let toggleButtons;
let dataPoint;

const dataLayerEvent = {
  event: 'Financial Well-Being Tool Interaction',
  action: 'Compare By Button Clicked',
  label: 'Age',
  eventCallback: undefined, // eslint-disable-line no-undefined
  eventTimeout: 500
};

const HTML_SNIPPET = `
<div class="content">
  <div class="o-expandable">
    <button class="o-expandable_target">
      <div class="o-expandable_header">
        <span class="o-expandable_header-left o-expandable_label">
        </span>
        <span class="o-expandable_header-right o-expandable_link">
          <span class="o-expandable_cue o-expandable_cue-open"></span>
          <span class="o-expandable_cue o-expandable_cue-close"></span>
        </span>
      </div>
    </button>
    <div class="o-expandable_content">
      <div class="o-expandable_content-animated"></div>
    </div>
  </div>
  <figure class="comparison-chart" id="comparison-chart">
    <div class="comparison-chart_toggle u-js-only">
      <h4>Compare by</h4>
      <button class="a-btn
                     comparison-chart_toggle-button
                     comparison-chart_toggle-button__selected"
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
      <dd>
        <span style="left: 49.3827160494%; border-color: #a6a329;">
          54
        </span>
      </dd>
      <dt class="comparison_data-point age_group">18-24 year olds</dt>
      <dd class="comparison_data-point age_mean">
        <span style="left: 45.6790123457%; border-color: #a6a329;">
          51
        </span>
      </dd>
      <dt class="comparison_data-point employment_group">Self-employed</dt>
      <dd class="comparison_data-point employment_mean">
        <span style="left: 49.3827160494%; border-color: #a6a329;">
          54
        </span>
      </dd>
      <dt class="comparison_data-point income_group">Less than $20,000</dt>
      <dd class="comparison_data-point income_mean">
        <span style="left: 39.5061728395%; border-color: #f9921c;">
          46
        </span>
      </dd>
    </dl>
  </figure>
</div>
`;

function initFwbResults() {
  fwbResults.init();
}

describe( 'fwb-results', () => {
  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
    window.dataLayer = [];
    window['google_tag_manager'] = {};

    toggleButtons = document.querySelectorAll(
      '.comparison-chart_toggle-button'
    );
    dataPoint = document.querySelectorAll(
      '.comparison_data-point'
    );
    expandableContent = document.querySelector( '.o-expandable_content' );
    expandableTarget = document.querySelector( '.o-expandable_target' );
    initFwbResults();
  } );

  // TODO: Add aria pressed states to cf-expandables
  xit( 'initialize the expandables on page load', () => {
    expect( expandableTarget.getAttribute( 'aria-pressed' ) ).toBe( 'false' );
    expect( expandableContent.getAttribute( 'aria-expanded' ) ).toBe( 'false' );
  } );

  it( 'should submit the correct analytics when a toggle button is clicked',
    () => {
      simulateEvent( 'click', toggleButtons[0] );

      expect( window.dataLayer[0] ).toStrictEqual( dataLayerEvent );
    }
  );

  it( 'should show the initial category on page load', () => {
    expect( toggleButtons[0].classList.contains( SELECTED_CLASS ) )
      .toBe( true );
    expect( dataPoint[0].classList.contains( HIDDEN_CLASS ) ).toBe( false );
    expect( dataPoint[1].classList.contains( HIDDEN_CLASS ) ).toBe( false );
  } );

  it( 'should hide the other categories on page load', () => {
    expect( toggleButtons[1].classList.contains( SELECTED_CLASS ) )
      .toBe( false );
    expect( dataPoint[4].classList.contains( HIDDEN_CLASS ) ).toBe( true );
    expect( dataPoint[5].classList.contains( HIDDEN_CLASS ) ).toBe( true );
  } );

  it( 'should hide the initial category content ' +
       'when a differnt toggle is clicked', () => {
    simulateEvent( 'click', toggleButtons[1] );
    expect( toggleButtons[0].classList.contains( SELECTED_CLASS ) )
      .toBe( false );
    expect( dataPoint[0].classList.contains( HIDDEN_CLASS ) ).toBe( true );
    expect( dataPoint[1].classList.contains( HIDDEN_CLASS ) ).toBe( true );
  } );

  it( 'should show the correct category content ' +
       'when the toggle is clicked', () => {
    simulateEvent( 'click', toggleButtons[1] );
    expect( toggleButtons[1].classList.contains( SELECTED_CLASS ) )
      .toBe( true );
    expect( dataPoint[4].classList.contains( HIDDEN_CLASS ) ).toBe( false );
    expect( dataPoint[5].classList.contains( HIDDEN_CLASS ) ).toBe( false );
  } );
} );
