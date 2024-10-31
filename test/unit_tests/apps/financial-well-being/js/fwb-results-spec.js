import fwbResults from '../../../../../cfgov/unprocessed/apps/financial-well-being/js/fwb-results.js';
import { simulateEvent } from '../../../../util/simulate-event.js';

const SELECTED_CLASS = 'comparison-chart__toggle-button--selected';
const HIDDEN_CLASS = 'u-hidden';

let expandableContent;
let expandableTarget;
let toggleButtons;
let dataPoint;

const dataLayerEvent = {
  event: 'Financial Well-Being Tool Interaction',
  action: 'Compare By Button Clicked',
  label: 'Age',
  eventCallback: undefined,
  eventTimeout: 500,
};

const HTML_SNIPPET = `
<div class="content">
  <div class="o-expandable">
    <button class="o-expandable__header">
      <span class="o-expandable__label">
      </span>
      <span class="o-expandable__cues">
        <span class="o-expandable__cue-open" role="img" aria-label="Show"></span>
        <span class="o-expandable__cue-close" role="img" aria-label="Hide"></span>
      </span>
    </button>
    <div class="o-expandable__content"></div>
  </div>
  <figure class="comparison-chart" id="comparison-chart">
    <div class="comparison-chart__toggle u-js-only">
      <h4>Compare by</h4>
      <button class="a-btn
                     comparison-chart__toggle-button
                     comparison-chart__toggle-button--selected"
              data-compare-by="age"
              data-gtm-action="Compare By Button Clicked"
              data-gtm-label="Age"
              data-gtm-category="Financial Well-Being Tool Interaction">
        Age
      </button>
      <button class="a-btn comparison-chart__toggle-button"
              data-compare-by="income"
              data-gtm-action="Compare By Button Clicked"
              data-gtm-label="Household income"
              data-gtm-category="Financial Well-Being Tool Interaction">
        Household income
      </button>
      <button class="a-btn comparison-chart__toggle-button"
              data-compare-by="employment"
              data-gtm-action="Compare By Button Clicked"
              data-gtm-label="Employment status"
              data-gtm-category="Financial Well-Being Tool Interaction">
        Employment status
      </button>
    </div>
    <dl class="comparison-chart__list">
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
      <dt class="comparison__data-point age__group">18-24 year olds</dt>
      <dd class="comparison__data-point age__mean">
        <span style="left: 45.6790123457%; border-color: #a6a329;">
          51
        </span>
      </dd>
      <dt class="comparison__data-point employment__group">Self-employed</dt>
      <dd class="comparison__data-point employment__mean">
        <span style="left: 49.3827160494%; border-color: #a6a329;">
          54
        </span>
      </dd>
      <dt class="comparison__data-point income__group">Less than $20,000</dt>
      <dd class="comparison__data-point income__mean">
        <span style="left: 39.5061728395%; border-color: #f9921c;">
          46
        </span>
      </dd>
    </dl>
  </figure>
</div>
`;

/**
 * Initialize the financial well-being results.
 */
function initFwbResults() {
  fwbResults.init();
}

describe('fwb-results', () => {
  beforeEach(() => {
    document.body.innerHTML = HTML_SNIPPET;
    window.dataLayer = [];
    window['google_tag_manager'] = {};

    toggleButtons = document.querySelectorAll(
      '.comparison-chart__toggle-button',
    );
    dataPoint = document.querySelectorAll('.comparison__data-point');
    expandableTarget = document.querySelector('.o-expandable__header');
    expandableContent = document.querySelector('.o-expandable__content');
    initFwbResults();
  });

  it('initialize the expandables on page load', () => {
    expect(expandableTarget.getAttribute('aria-expanded')).toBe('false');
    expect(expandableContent.getAttribute('data-open')).toBe('false');
  });

  it('should submit the correct analytics when a toggle button is clicked', () => {
    simulateEvent('click', toggleButtons[0]);
    setTimeout(() => {
      expect(window.dataLayer[0]).toStrictEqual(dataLayerEvent);
    }, 500);
  });

  it('should show the initial category on page load', () => {
    expect(toggleButtons[0].classList.contains(SELECTED_CLASS)).toBe(true);
    expect(dataPoint[0].classList.contains(HIDDEN_CLASS)).toBe(false);
    expect(dataPoint[1].classList.contains(HIDDEN_CLASS)).toBe(false);
  });

  it('should hide the other categories on page load', () => {
    expect(toggleButtons[1].classList.contains(SELECTED_CLASS)).toBe(false);
    expect(dataPoint[4].classList.contains(HIDDEN_CLASS)).toBe(true);
    expect(dataPoint[5].classList.contains(HIDDEN_CLASS)).toBe(true);
  });

  it(
    'should hide the initial category content ' +
      'when a differnt toggle is clicked',
    () => {
      simulateEvent('click', toggleButtons[1]);
      expect(toggleButtons[0].classList.contains(SELECTED_CLASS)).toBe(false);
      expect(dataPoint[0].classList.contains(HIDDEN_CLASS)).toBe(true);
      expect(dataPoint[1].classList.contains(HIDDEN_CLASS)).toBe(true);
    },
  );

  it('should show the correct category content when the toggle is clicked', () => {
    simulateEvent('click', toggleButtons[1]);
    expect(toggleButtons[1].classList.contains(SELECTED_CLASS)).toBe(true);
    expect(dataPoint[4].classList.contains(HIDDEN_CLASS)).toBe(false);
    expect(dataPoint[5].classList.contains(HIDDEN_CLASS)).toBe(false);
  });
});
