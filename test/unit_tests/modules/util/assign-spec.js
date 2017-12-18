const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

const chai = require( 'chai' );
const expect = chai.expect;
const assign = require( BASE_JS_PATH + 'modules/util/assign.js' ).assign;
let testObjectA;
let testObjectB;
let testObjectC;
let undefinedVar;


beforeEach( () => {

  testObjectA = {
    str:  'test',
    func: () => 'testStr',
    num:  1
  };

  testObjectB = {
    obj:   { test: 2 },
    arr:   [ 3 ],
    _null: null
  };

  testObjectC = {
    bool:  Boolean( false ),
    undef: undefinedVar,
    num:   4
  };

} );

describe( 'Assign', () => {

  it( 'should assign properties from source to destination', () => {
    assign( testObjectA, testObjectB );

    expect( testObjectA.hasOwnProperty( 'obj' ) ).to.be.true;
    expect( testObjectA.hasOwnProperty( 'arr' ) ).to.be.true;
    expect( testObjectA.hasOwnProperty( '_null' ) ).to.be.true;
  } );

  it( 'should assign values from source to destination', () => {
    assign( testObjectA, testObjectB );

    expect( testObjectA.obj.test === 2 ).to.be.true;
    expect( testObjectA.arr[0] === 3 ).to.be.true;
    expect( testObjectA._null === null ).to.be.true;
  } );

  it( 'should assign multiple source properties to destination', () => {
    assign( testObjectA, testObjectB, testObjectC );

    expect( testObjectA.hasOwnProperty( 'bool' ) ).to.be.true;
    expect( testObjectA.hasOwnProperty( 'undef' ) ).to.be.true;
    expect( testObjectA.hasOwnProperty( 'num' ) ).to.be.true;
  } );

  it( 'should assign multiple source values to destination', () => {
    assign( testObjectA, testObjectB, testObjectC );

    expect( testObjectA.bool === false ).to.be.true;
    expect( typeof testObjectA.undef === 'undefined' ).to.be.true;
    expect( testObjectA.num === 4 ).to.be.true;
  } );

  it( 'should selectively overwrite existing source properties', () => {
    expect( testObjectA.num === 1 ).to.be.true;

    assign( testObjectA, testObjectC );

    expect( testObjectA.str === 'test' ).to.be.true;
    expect( testObjectA.func() === 'testStr' ).to.be.true;
    expect( testObjectA.num === 4 ).to.be.true;
  } );

} );
