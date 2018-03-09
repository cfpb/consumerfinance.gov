const BASE_JS_PATH = '../../../../../../cfgov/unprocessed/apps/owning-a-home/';
const chai = require( 'chai' );
const expect = chai.expect;

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
    expect( params.getVal( 'credit-score' ) ).to.equal( 700 );
    expect( params.getVal( 'down-payment' ) ).to.equal( '20,000' );
    expect( params.getVal( 'house-price' ) ).to.equal( '200,000' );
    expect( params.getVal( 'loan-amount' ) ).to.be.undefined;
    expect( params.getVal( 'location' ) ).to.equal( 'AL' );
    expect( params.getVal( 'rate-structure' ) ).to.equal( 'fixed' );
    expect( params.getVal( 'loan-term' ) ).to.equal( 30 );
    expect( params.getVal( 'loan-type' ) ).to.equal( 'conf' );
    expect( params.getVal( 'arm-type' ) ).to.equal( '5-1' );
    expect( params.getVal( 'edited' ) ).to.be.false;
    expect( params.getVal( 'isJumbo' ) ).to.be.false;
    expect( params.getVal( 'prevLoanType' ) ).to.equal( '' );
    expect( params.getVal( 'prevLocation' ) ).to.equal( '' );
    expect( params.getVal( 'verbotenKeys' ) ).to.be.an( 'array' );
    expect( params.getVal( 'verbotenKeys' )[0] ).to.equal( 9 );
    expect( params.getVal( 'verbotenKeys' )[1] ).to.equal( 37 );
    expect( params.getVal( 'verbotenKeys' )[2] ).to.equal( 38 );
    expect( params.getVal( 'verbotenKeys' )[3] ).to.equal( 39 );
    expect( params.getVal( 'verbotenKeys' )[4] ).to.equal( 40 );
    expect( params.getVal( 'verbotenKeys' )[5] ).to.equal( 13 );
    expect( params.getVal( 'verbotenKeys' )[6] ).to.equal( 16 );
  } );

  it( 'should be able to set a value', () => {
    params.setVal( 'credit-score', 800 );
    expect( params.getVal( 'credit-score' ) ).to.equal( 800 );
  } );

  it( 'should be able to update a value from the HTML', () => {
    expect( params.getVal( 'prevLoanType' ) ).to.equal( '' );
    expect( params.getVal( 'prevLocation' ) ).to.equal( '' );
    params.update();
    expect( params.getVal( 'prevLoanType' ) ).to.equal( 'conf' );
    expect( params.getVal( 'prevLocation' ) ).to.equal( 'AL' );

    const sliderElement = document.querySelector( '#credit-score' );
    expect( params.getVal( 'credit-score' ) ).to.equal( 700 );
    sliderElement.value = 800;
    params.update();
    expect( params.getVal( 'credit-score' ) ).to.equal( 800 );
  } );
} );
