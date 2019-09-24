const BASE_JS_PATH = '../../../../../../unprocessed/apps/owning-a-home/';

const HTML_SNIPPET = `
  <input id="credit-score"
         type="range" min="600" max="840" step="20" value="700">
  <input id="down-payment" type="text" placeholder="20,000">
  <input id="house-price" type="text" placeholder="200,000">
  <input id="loan-amount" type="text" placeholder="200,000">
  <select id="location">
      <option value="VT">Vermont</option>
  </select>
  <select id="rate-structure">
    <option value="fixed">Fixed</option>
    <option value="arm">Adjustable</option>
  </select>
  <select id="loan-term">
      <option value="30">30 Years</option>
      <option value="15">15 Years</option>
  </select>
  <select id="loan-type">
      <option value="conf">Conventional</option>
      <option value="fha">FHA</option>
      <option value="va">VA</option>
  </select>
  <select id="arm-type">
      <option value="3-1">3/1</option>
      <option value="5-1">5/1</option>
      <option value="7-1">7/1</option>
      <option value="10-1">10/1</option>
  </select>
`;

const params = require( BASE_JS_PATH + 'js/explore-rates/params' );

describe( 'explore-rates/params', () => {
  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
  } );

  it( 'should be able to get a value', () => {
    expect( params.getVal( 'credit-score' ) ).toBe( 700 );
    expect( params.getVal( 'down-payment' ) ).toBe( '20,000' );
    expect( params.getVal( 'dp-constant' ) ).toBe( '' );
    expect( params.getVal( 'house-price' ) ).toBe( '200,000' );
    expect( params.getVal( 'loan-amount' ) ).toBeUndefined();
    expect( params.getVal( 'location' ) ).toBe( 'AL' );
    expect( params.getVal( 'rate-structure' ) ).toBe( 'fixed' );
    expect( params.getVal( 'loan-term' ) ).toBe( 30 );
    expect( params.getVal( 'loan-type' ) ).toBe( 'conf' );
    expect( params.getVal( 'arm-type' ) ).toBe( '5-1' );
    expect( params.getVal( 'edited' ) ).toBe( false );
    expect( params.getVal( 'isJumbo' ) ).toBe( false );
    expect( params.getVal( 'prevLoanType' ) ).toBe( '' );
    expect( params.getVal( 'prevLocation' ) ).toBe( '' );
    expect( params.getVal( 'request' ) ).toBeUndefined();
  } );

  it( 'should be able to set a value', () => {
    params.setVal( 'credit-score', 800 );
    expect( params.getVal( 'credit-score' ) ).toBe( 800 );
  } );

  it( 'should be able to return all stored values', () => {
    let UNDEFINED;
    const mockData = {
      'credit-score':   800,
      'down-payment':   '20,000',
      'dp-constant':    '',
      'house-price':    '200,000',
      'location':       'AL',
      'loan-amount':    UNDEFINED,
      'rate-structure': 'fixed',
      'loan-term':      30,
      'loan-type':      'conf',
      'arm-type':       '5-1',
      'edited':         false,
      'isJumbo':        false,
      'prevLoanType':   '',
      'prevLocation':   '',
      'request':        UNDEFINED
    };
    const storedValues = params.getAllParams();
    expect( storedValues ).toStrictEqual( mockData );
  } );

  it( 'should be able to update a value from the HTML', () => {
    expect( params.getVal( 'prevLoanType' ) ).toBe( '' );
    expect( params.getVal( 'prevLocation' ) ).toBe( '' );
    params.update();
    expect( params.getVal( 'prevLoanType' ) ).toBe( 'conf' );
    expect( params.getVal( 'prevLocation' ) ).toBe( 'AL' );

    const sliderElement = document.querySelector( '#credit-score' );
    expect( params.getVal( 'credit-score' ) ).toBe( 700 );
    sliderElement.value = 800;
    params.update();
    expect( params.getVal( 'credit-score' ) ).toBe( 800 );
  } );
} );
