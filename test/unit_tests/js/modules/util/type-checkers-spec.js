import * as typeCheckers from '../../../../../unprocessed/js/modules/util/type-checkers.js';

let undefinedVar;
const blankVar = '';
const aString = 'bar';
const aNum = 42;
const aDate = new Date( 2011, 7, 21 );
function aFunction() {
  return true;
}
const anObject = {
  a: '1',
  b: '2',
  c: '3'
};
const anArray = [ 1, 2, 3 ];

describe( 'TypeCheckers isUndefined', () => {
  it( 'should identify undefined variables', () => {
    expect( typeCheckers.isUndefined( undefinedVar ) ).toBe( true );
  } );

  it( 'should NOT return true for blank variables', () => {
    expect( typeCheckers.isUndefined( blankVar ) ).toBe( false );
  } );

  it( 'should NOT return true for defined variables', () => {
    expect( typeCheckers.isUndefined( aString ) ).toBe( false );
  } );
} );

describe( 'TypeCheckers isDefined', () => {
  it( 'should return true for defined variables', () => {
    expect( typeCheckers.isDefined( aString ) ).toBe( true );
  } );

  it( 'should return true for blank variables', () => {
    expect( typeCheckers.isDefined( blankVar ) ).toBe( true );
  } );

  it( 'should NOT return true for undefined variables', () => {
    expect( typeCheckers.isDefined( undefinedVar ) ).toBe( false );
  } );
} );

describe( 'TypeCheckers isObject', () => {
  it( 'should return true for objects', () => {
    expect( typeCheckers.isObject( anObject ) ).toBe( true );
  } );

  it( 'should return false for strings', () => {
    expect( typeCheckers.isObject( aString ) ).toBe( false );
  } );
} );

describe( 'TypeCheckers isString', () => {
  it( 'should return true for strings', () => {
    expect( typeCheckers.isString( aString ) ).toBe( true );
  } );

  it( 'should return false for objects', () => {
    expect( typeCheckers.isString( anObject ) ).toBe( false );
  } );
} );

describe( 'TypeCheckers isNumber', () => {
  it( 'should return true for numbers', () => {
    expect( typeCheckers.isNumber( aNum ) ).toBe( true );
  } );

  it( 'should return false for strings', () => {
    expect( typeCheckers.isNumber( aString ) ).toBe( false );
    expect( typeCheckers.isNumber( '42' ) ).toBe( false );
  } );
} );

describe( 'TypeCheckers isDate', () => {
  it( 'should return true for dates', () => {
    expect( typeCheckers.isDate( aDate ) ).toBe( true );
  } );

  it( 'should return false for numbers', () => {
    expect( typeCheckers.isDate( aNum ) ).toBe( false );
  } );
} );

describe( 'TypeCheckers isArray', () => {
  it( 'should return true for arrays', () => {
    expect( typeCheckers.isArray( anArray ) ).toBe( true );
  } );

  it( 'should return false for objects', () => {
    expect( typeCheckers.isArray( anObject ) ).toBe( false );
  } );
} );

describe( 'TypeCheckers isFunction', () => {
  it( 'should return true for a functions', () => {
    expect( typeCheckers.isFunction( aFunction ) ).toBe( true );
  } );

  it( 'should return false for a non-function', () => {
    expect( typeCheckers.isFunction( aString ) ).toBe( false );
  } );
} );

describe( 'TypeCheckers isEmpty', () => {
  it( 'should return true for empty vars', () => {
    expect( typeCheckers.isEmpty( blankVar ) ).toBe( true );
  } );

  it( 'should return false for non-empty vars', () => {
    expect( typeCheckers.isEmpty( aString ) ).toBe( false );
  } );
} );
