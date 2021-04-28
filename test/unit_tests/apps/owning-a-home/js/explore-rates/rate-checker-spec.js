import * as rateChecker from '../../../../../../cfgov/unprocessed/apps/owning-a-home/js/explore-rates/rate-checker';
import {
  axios
} from '../../../../../../cfgov/unprocessed/apps/owning-a-home/node_modules/axios';
import { simulateEvent } from '../../../../../util/simulate-event';

// Mock the XmlHttpRequest call from axios.
jest.mock(
  '../../../../../../cfgov/unprocessed/apps/owning-a-home/node_modules/axios'
);
const mockResp = { data: 'mock data' };
axios.get.mockImplementation( () => Promise.resolve( mockResp ) );

const HTML_SNIPPET = `
<div class="rate-checker">
  <div id="rate-results">
    <div id="accessible-data-results">
      <table id="accessible-data">
        <tbody>
          <tr class="table-head">
            <th>Loan Rates</th>
          </tr>
          <tr class="table-body">
            <td>number of corresponding rates</td>
          </tr>
        </tbody>
      </table>
    </div>

    <section id="chart-section" class="chart">

      <figure class="data-enabled loading">
          <div id="chart" class="chart-area"></div>
          <figcaption class="chart-caption">
              <div class="caption-title">
                  Interest rates for your situation
              </div>
              <div class="rc-data-link">
                  <a href="#about" class="u-link-underline">
                      About our data source
                  </a>
              </div>
          </figcaption>
      </figure>

      <div id="chart-result-alert"
           class="result-alert chart-alert u-hidden"
           role="alert">
      </div>

      <div id="chart-fail-alert"
           class="result-alert chart-alert u-hidden"
           role="alert">
      </div>

    </section>
  </div>
  <div class="result">
    <div class="calculator">

      <section id="credit-score-container">
        <div class="a-range" id="credit-score-range">
          <div class="a-range_labels">
            <span class="a-range_labels-min"></span>
            <span class="a-range_labels-max"></span>
          </div>
          <input type="range"
                 class="a-range_input">
          <div class="a-range_text"></div>
        </div>

        <div id="credit-score-alert"
             class="result-alert chart-alert u-hidden"
             role="alert">
        </div>
      </section>

      <section class="calc-loan-amt" id="loan-amt-inputs">
          <div class="house-price half-width-gt-1230">
              <label for="house-price">House price</label>
              <div class="dollar-input">
                  <span class="unit">$</span>
                  <input type="text" placeholder="200,000" name="house-price"
                         class="recalc" id="house-price">
              </div>
          </div>
          <div class="down-payment half-width-gt-1230">
              <label for="down-payment">Down payment</label>
              <div class="percent-input">
                  <span class="unit">%</span>
                  <input type="text" placeholder="10"
                         name="percent-down" maxlength="2"
                         class="recalc" id="percent-down">
              </div>
              <div class="dollar-input">
                  <span class="unit">$</span>
                  <input type="text" placeholder="20,000" name="down-payment"
                         class="recalc" "="" id="down-payment" value="20000">
              </div>
          </div>
          <div class="loan-amt-total half-width-gt-1230">
              <label class="inline">Loan amount</label>
              <span id="loan-amount-result">$180,000</span>
          </div>
          <div class="county half-width-gt-1230 u-hidden">
              <label for="county">County</label>
              <div class="select-content a-select">
                  <select name="county" class="recalc" id="county">
                  </select>
              </div>
          </div>

          <div id="dp-alert"
               class="downpayment-warning alert-alt col-7 u-hidden"
               role="alert">
            Your down payment cannot be more than your house price.
          </div>
      </section>

      <section class="calc-loan-details">

        <div class="upper rate-structure half-width-gt-1230">
            <label for="rate-structure">Rate type</label>
            <div class="select-content a-select">
                <select name="rate-structure" class="recalc" id="rate-structure">
                    <option value="fixed">Fixed</option>
                    <option value="arm">Adjustable</option>
                </select>
            </div>
        </div>

        <div class="arm-type half-width-gt-1230 u-hidden">
            <label for="arm-type">ARM type</label>
            <div class="select-content a-select">
                <select name="arm-type" class="recalc" id="arm-type">
                    <option value="3-1">3/1</option>
                    <option value="5-1">5/1</option>
                    <option value="7-1">7/1</option>
                    <option value="10-1">10/1</option>
                </select>
            </div>
        </div>
      </section>

      <section class="form-sub warning u-hidden" id="arm-warning">
        <p class="warning-text">While some lenders may offer FHA, VA, or 15-year adjustable-rate mortgages, they are rare. We don’t have enough data to display results for these combinations. Choose a fixed rate if you’d like to try these options.</p>
      </section>
    </div>
  </div>
  <div class="rc-results" id="rate-results" aria-live="polite">
    <section class="compare wrapper data-enabled loaded">
      <div id="rate-selects">
      </div>
    </section>
  </div>
</div>
`;

let downPaymentDom;
let rateStructureDom;
let armTypeDom;

describe( 'explore-rates/rate-checker', () => {
  describe( 'init()', () => {
    beforeEach( () => {
      document.body.innerHTML = HTML_SNIPPET;
    } );

    it( 'should not initialize when rate-checker class isn\'t found', () => {
      document.body.innerHTML = '';
      expect( rateChecker.init() ).toBe( false );
    } );

    it( 'should initialize when rate-checker class is found', () => {
      expect( rateChecker.init() ).toBe( true );
    } );

  } );

  describe( 'interactions', () => {
    beforeEach( () => {
      document.body.innerHTML = HTML_SNIPPET;
      downPaymentDom = document.querySelector( '#down-payment' );
      rateStructureDom = document.querySelector( '#rate-structure' );
      armTypeDom = document.querySelector( '#arm-type' );
      rateChecker.init();
    } );

    it( 'Should process value in down payment when leaving focus', () => {
      expect( downPaymentDom.value ).toBe( '20000' );
      simulateEvent( 'focusout', downPaymentDom );
      expect( downPaymentDom.value ).toBe( '20,000' );
    } );

    it( 'rate structure', () => {
      expect( rateStructureDom.value ).toBe( 'fixed' );
    } );

    it( 'ARM type', () => {
      expect( armTypeDom.value ).toBe( '5-1' );
    } );
  } );
} );
