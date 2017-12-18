const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

const chai = require( 'chai' );
const expect = chai.expect;
const standardType = require( BASE_JS_PATH + 'modules/util/standard-type' );

describe( 'standard-type', () => {
  it( 'should include a standard JS data hook', () => {
    expect( standardType.JS_HOOK ).to.equal( 'data-js-hook' );
  } );

  it( 'should include a non operational function', () => {
    expect( standardType.noopFunct() ).to.be.undefined;
  } );

  it( 'should include a standard undefined reference', () => {
    expect( standardType.UNDEFINED ).to.be.undefined;
  } );
} );
