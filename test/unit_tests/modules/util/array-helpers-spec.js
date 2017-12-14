const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

const chai = require( 'chai' );
const expect = chai.expect;
const arrayHelpers = require( BASE_JS_PATH + 'modules/util/array-helpers' );
let array;
let index;

describe( 'Array Helpers indexOfObject', () => {

  it( 'should return -1 if the array is empty', () => {
    array = [];
    index = arrayHelpers.indexOfObject( array, 'foo' );

    expect( index ).to.equal( -1 );
  } );

  it( 'should return -1 if there is no match', () => {
    array = [
      { value: 'bar' },
      { value: 'baz' }
    ];
    index = arrayHelpers.indexOfObject( array, 'value', 'foo' );

    expect( index ).to.equal( -1 );
  } );

  it( 'should return the matched index', () => {
    array = [
      { value: 'foo' },
      { value: 'bar' },
      { value: 'baz' }
    ];
    index = arrayHelpers.indexOfObject( array, 'value', 'foo' );

    expect( index ).to.equal( 0 );
  } );
} );
