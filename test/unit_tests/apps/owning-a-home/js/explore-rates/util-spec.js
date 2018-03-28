const BASE_JS_PATH = '../../../../../../cfgov/unprocessed/apps/owning-a-home/';
const util = require( BASE_JS_PATH + 'js/explore-rates/util' );

const HTML_SNIPPET = `
  <strong id="timestamp"></strong>
  <span id="loan-amount-result"></span>
`;

let timeStampDom;
let loanAmountResultDom;

describe( 'explore-rates/util', () => {
  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
    timeStampDom = document.querySelector( '#timestamp' );
    loanAmountResultDom = document.querySelector( '#loan-amount-result' );
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

  describe( 'formatTimestampMMddyyyy()', () => {
    it( 'should format a timestamp as a date.', () => {
      expect( util.formatTimestampMMddyyyy( '2018-03-14T04:00:00Z' ) )
        .toBe( '03/14/2018' );
    } );
  } );

  describe( 'renderDatestamp()', () => {
    it( 'should format a timestamp as a date.', () => {
      util.renderDatestamp( timeStampDom, '2018-03-14T04:00:00Z' );
      expect( timeStampDom.textContent ).toBe( '03/14/2018' );
    } );
  } );

  describe( 'renderLoanAmount()', () => {
    it( 'should format a timestamp as a date.', () => {
      util.renderLoanAmount( loanAmountResultDom, 180000 );
      expect( loanAmountResultDom.textContent ).toBe( '$180,000' );
    } );
  } );
} );
