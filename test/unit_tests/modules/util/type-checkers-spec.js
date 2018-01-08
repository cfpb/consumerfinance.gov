const chai = require( 'chai' );
const expect = chai.expect;
const typeCheckers = require(
  '../../../../cfgov/unprocessed/js/modules/util/type-checkers.js'
);

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
    expect( typeCheckers.isUndefined( undefinedVar ) ).to.be.true;
  } );

  it( 'should NOT return true for blank variables', () => {
    expect( typeCheckers.isUndefined( blankVar ) ).to.be.false;
  } );

  it( 'should NOT return true for defined variables', () => {
    expect( typeCheckers.isUndefined( aString ) ).to.be.false;
  } );
} );

describe( 'TypeCheckers isDefined', () => {
  it( 'should return true for defined variables', () => {
    expect( typeCheckers.isDefined( aString ) ).to.be.true;
  } );

  it( 'should return true for blank variables', () => {
    expect( typeCheckers.isDefined( blankVar ) ).to.be.true;
  } );

  it( 'should NOT return true for undefined variables', () => {
    expect( typeCheckers.isDefined( undefinedVar ) ).to.be.false;
  } );
} );

describe( 'TypeCheckers isObject', () => {
  it( 'should return true for objects', () => {
    expect( typeCheckers.isObject( anObject ) ).to.be.true;
  } );

  it( 'should return false for strings', () => {
    expect( typeCheckers.isObject( aString ) ).to.be.false;
  } );
} );

describe( 'TypeCheckers isString', () => {
  it( 'should return true for strings', () => {
    expect( typeCheckers.isString( aString ) ).to.be.true;
  } );

  it( 'should return false for objects', () => {
    expect( typeCheckers.isString( anObject ) ).to.be.false;
  } );
} );

describe( 'TypeCheckers isNumber', () => {
  it( 'should return true for numbers', () => {
    expect( typeCheckers.isNumber( aNum ) ).to.be.true;
  } );

  it( 'should return false for strings', () => {
    expect( typeCheckers.isNumber( aString ) ).to.be.false;
    expect( typeCheckers.isNumber( '42' ) ).to.be.false;
  } );
} );

describe( 'TypeCheckers isDate', () => {
  it( 'should return true for dates', () => {
    expect( typeCheckers.isDate( aDate ) ).to.be.true;
  } );

  it( 'should return false for numbers', () => {
    expect( typeCheckers.isDate( aNum ) ).to.be.false;
  } );
} );

describe( 'TypeCheckers isArray', () => {
  it( 'should return true for arrays', () => {
    expect( typeCheckers.isArray( anArray ) ).to.be.true;
  } );

  it( 'should return false for objects', () => {
    expect( typeCheckers.isArray( anObject ) ).to.be.false;
  } );
} );

describe( 'TypeCheckers isFunction', () => {
  it( 'should return true for a functions', () => {
    expect( typeCheckers.isFunction( aFunction ) ).to.be.true;
  } );

  it( 'should return false for a non-function', () => {
    expect( typeCheckers.isFunction( aString ) ).to.be.false;
  } );
} );

describe( 'TypeCheckers isEmpty', () => {
  it( 'should return true for empty vars', () => {
    expect( typeCheckers.isEmpty( blankVar ) ).to.be.true;
  } );

  it( 'should return false for non-empty vars', () => {
    expect( typeCheckers.isEmpty( aString ) ).to.be.false;
  } );
} );
