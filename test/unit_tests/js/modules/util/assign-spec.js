const BASE_JS_PATH = '../../../../../unprocessed/js/';
const assign = require( BASE_JS_PATH + 'modules/util/assign.js' ).assign;
let testObjectA;
let testObjectB;
let testObjectC;
let undefinedVar;

describe( 'Assign', () => {
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

  it( 'should assign properties from source to destination', () => {
    assign( testObjectA, testObjectB );

    expect( testObjectA.hasOwnProperty( 'obj' ) ).toBe( true );
    expect( testObjectA.hasOwnProperty( 'arr' ) ).toBe( true );
    expect( testObjectA.hasOwnProperty( '_null' ) ).toBe( true );
  } );

  it( 'should assign values from source to destination', () => {
    assign( testObjectA, testObjectB );

    expect( testObjectA.obj.test === 2 ).toBe( true );
    expect( testObjectA.arr[0] === 3 ).toBe( true );
    expect( testObjectA._null === null ).toBe( true );
  } );

  it( 'should assign multiple source properties to destination', () => {
    assign( testObjectA, testObjectB, testObjectC );

    expect( testObjectA.hasOwnProperty( 'bool' ) ).toBe( true );
    expect( testObjectA.hasOwnProperty( 'undef' ) ).toBe( true );
    expect( testObjectA.hasOwnProperty( 'num' ) ).toBe( true );
  } );

  it( 'should assign multiple source values to destination', () => {
    assign( testObjectA, testObjectB, testObjectC );

    expect( testObjectA.bool === false ).toBe( true );
    expect( typeof testObjectA.undef === 'undefined' ).toBe( true );
    expect( testObjectA.num === 4 ).toBe( true );
  } );

  it( 'should selectively overwrite existing source properties', () => {
    expect( testObjectA.num === 1 ).toBe( true );

    assign( testObjectA, testObjectC );

    expect( testObjectA.str === 'test' ).toBe( true );
    expect( testObjectA.func() === 'testStr' ).toBe( true );
    expect( testObjectA.num === 4 ).toBe( true );
  } );

} );
