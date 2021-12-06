const BASE_JS_PATH = '../../../../../../cfgov/unprocessed/apps/owning-a-home/';
const util = require( BASE_JS_PATH + 'js/explore-rates/util' );

const HTML_SNIPPET = `
  <input id="credit-score" type="range" min="0" max="100" value="50">
  <strong id="timestamp"></strong>
  <span id="loan-amount-result"></span>
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
  <div class="result">
    <div class="house-price">
      <label for="house-price">House price</label>
      <div class="dollar-input">
        <span class="unit">$</span>
        <input type="text" name="house-price" id="house-price" placeholder="0">
      </div>
    </div>
    <div class="down-payment>
        <label for="down-payment">Down payment</label>
        <div class="percent-input">
            <span class="unit">%</span>
            <input type="text" name="percent-down" maxlength="2" id="percent-down">
        </div>
        <div class="dollar-input">
            <span class="unit">$</span>
            <input type="text" name="down-payment" id="down-payment" value='0'>
        </div>
    </div>
  </div>
`;

let downPaymentDom;
let housePriceDom;
let timeStampDom;
let loanAmountResultDom;
let accessibleDataDom;
let accessibleDataTableHeadDom;
let accessibleDataTableBodyDom;

describe( 'explore-rates/util', () => {
  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
    timeStampDom = document.querySelector( '#timestamp' );
    loanAmountResultDom = document.querySelector( '#loan-amount-result' );
    accessibleDataDom = document.querySelector( '#accessible-data' );
    accessibleDataTableHeadDom =
      accessibleDataDom.querySelector( '.table-head' );
    accessibleDataTableBodyDom =
      accessibleDataDom.querySelector( '.table-body' );
  } );

  describe( 'removeDollarAddCommas()', () => {
    it( 'should return true if HTML element has u-hidden class.', () => {
      expect( util.removeDollarAddCommas( '$10000' ) ).toBe( '10,000' );
    } );
  } );

  describe( 'calcLoanAmount()', () => {
    it( 'should calculate a loan amount in USD ' +
        'given a house price and down payment amount.', () => {
      expect( util.calcLoanAmount( 200000, 20000 ) ).toBe( 180000 );
    } );

    it( 'should return 0 if loan amount is negative.', () => {
      expect( util.calcLoanAmount( 200000, 2000000 ) ).toBe( 0 );
    } );
  } );

  describe( 'checkIfZero()', () => {
    it( 'should return true if value is zero.', () => {
      expect( util.checkIfZero( '0' ) ).toBe( true );
      expect( util.checkIfZero( 0 ) ).toBe( true );
    } );

    it( 'should return false if value is NOT zero.', () => {
      expect( util.checkIfZero( '1' ) ).toBe( false );
      expect( util.checkIfZero( -1 ) ).toBe( false );
    } );
  } );

  describe( 'delay()', () => {
    it( 'should delay function execution.', () => {
      const testFunct = jest.fn();
      jest.useFakeTimers();
      jest.spyOn( global, 'setTimeout' );
      util.delay( testFunct, 500 );
      expect( setTimeout ).toHaveBeenLastCalledWith( testFunct, 500 );
    } );
  } );

  describe( 'formatTimestampMMddyyyy()', () => {
    it( 'should format a timestamp as a date.', () => {
      expect( util.formatTimestampMMddyyyy( '2018-03-14T12:00:00Z' ) )
        .toBe( '03/14/2018' );
    } );
  } );

  describe( 'isKeyAllowed()', () => {
    it( 'should return true if key code is not in forbidden list.', () => {
      expect( util.isKeyAllowed( 0 ) ).toBe( true );
    } );

    it( 'should return false if key code is in forbidden list.', () => {
      expect( util.isKeyAllowed( 9 ) ).toBe( false );
    } );
  } );

  describe( 'isVisible()', () => {
    it( 'should return true if HTML element has u-hidden class.', () => {
      expect( util.isVisible( timeStampDom ) ).toBe( true );
    } );

    it( 'should return false if HTML element does NOT have u-hidden class.',
      () => {
        timeStampDom.classList.add( 'u-hidden' );
        expect( util.isVisible( timeStampDom ) ).toBe( false );
      }
    );
  } );

  describe( 'renderAccessibleData()', () => {
    it( 'should format a timestamp as a date.', () => {
      const mockLabels = [ '4.500%', '4.625%' ];
      const mockVals = [ 3, 6 ];

      const tableHeadHtml = '<th>4.500%</th><th>4.625%</th>';
      const tableBodyHtml = '<td>3</td><td>6</td>';

      util.renderAccessibleData(
        accessibleDataTableHeadDom, accessibleDataTableBodyDom,
        mockLabels, mockVals
      );
      expect( accessibleDataTableHeadDom.innerHTML ).toBe( tableHeadHtml );
      expect( accessibleDataTableBodyDom.innerHTML ).toBe( tableBodyHtml );
    } );
  } );

  describe( 'renderDatestamp()', () => {
    it( 'should format a timestamp as a date.', () => {
      util.renderDatestamp( timeStampDom, '2018-03-14T12:00:00Z' );
      expect( timeStampDom.textContent ).toBe( '03/14/2018' );
    } );

    it( 'should format timestamp only if timestamp is passed.', () => {
      util.renderDatestamp( timeStampDom );
      expect( timeStampDom.textContent ).toBe( '' );
    } );
  } );

  describe( 'renderLoanAmount()', () => {
    it( 'should format a timestamp as a date.', () => {
      util.renderLoanAmount( loanAmountResultDom, 180000 );
      expect( loanAmountResultDom.textContent ).toBe( '$180,000' );
    } );
  } );

  describe( 'setSelections()', () => {
    it( 'should set value or attribute of element.', () => {
      downPaymentDom = document.querySelector( '#down-payment' );
      housePriceDom = document.querySelector( '#house-price' );
      const mockParams = {
        'down-payment': '20,000',
        'house-price':  '200,000'
      };
      expect( downPaymentDom.value ).toBe( '0' );
      expect( housePriceDom.getAttribute( 'placeholder' ) ).toBe( '0' );
      util.setSelections( mockParams );
      expect( downPaymentDom.value ).toBe( '20,000' );
      expect( housePriceDom.getAttribute( 'placeholder' ) ).toBe( '200,000' );
    } );
  } );
} );
