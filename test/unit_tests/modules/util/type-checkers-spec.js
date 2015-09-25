'use strict';
var chai = require( 'chai' );
var expect = chai.expect;
var typeCheckers = require(
  '../../../../cfgov/v1/preprocessed/js/modules/util/type-checkers.js'
);

var undefinedVar;
var blankVar = '';
var aString = 'bar';
var aNum = 42;
var aDate = new Date( 2011, 7, 21 );
function aFunction() {
  return true;
}
var anObject = {
  a: '1',
  b: '2',
  c: '3'
};
var anArray = [ 1, 2, 3 ];

describe( 'TypeCheckers isUndefined', function() {
  it( 'should identify undefined variables', function() {
    expect( typeCheckers.isUndefined( undefinedVar ) ).to.be.true;
  } );

  it( 'should NOT return true for blank variables', function() {
    expect( typeCheckers.isUndefined( blankVar ) ).to.be.false;
  } );

  it( 'should NOT return true for defined variables', function() {
    expect( typeCheckers.isUndefined( aString ) ).to.be.false;
  } );
} );

describe( 'TypeCheckers isDefined', function() {
  it( 'should return true for defined variables', function() {
    expect( typeCheckers.isDefined( aString ) ).to.be.true;
  } );

  it( 'should return true for blank variables', function() {
    expect( typeCheckers.isDefined( blankVar ) ).to.be.true;
  } );

  it( 'should NOT return true for undefined variables', function() {
    expect( typeCheckers.isDefined( undefinedVar ) ).to.be.false;
  } );
} );

describe( 'TypeCheckers isObject', function() {
  it( 'should return true for objects', function() {
    expect( typeCheckers.isObject( anObject ) ).to.be.true;
  } );

  it( 'should return false for strings', function() {
    expect( typeCheckers.isObject( aString ) ).to.be.false;
  } );
} );

describe( 'TypeCheckers isString', function() {
  it( 'should return true for strings', function() {
    expect( typeCheckers.isString( aString ) ).to.be.true;
  } );

  it( 'should return false for objects', function() {
    expect( typeCheckers.isString( anObject ) ).to.be.false;
  } );
} );

describe( 'TypeCheckers isNumber', function() {
  it( 'should return true for numbers', function() {
    expect( typeCheckers.isNumber( aNum ) ).to.be.true;
  } );

  it( 'should return false for strings', function() {
    expect( typeCheckers.isNumber( aString ) ).to.be.false;
    expect( typeCheckers.isNumber( '42' ) ).to.be.false;
  } );
} );

describe( 'TypeCheckers isDate', function() {
  it( 'should return true for dates', function() {
    expect( typeCheckers.isDate( aDate ) ).to.be.true;
  } );

  it( 'should return false for numbers', function() {
    expect( typeCheckers.isDate( aNum ) ).to.be.false;
  } );
} );

describe( 'TypeCheckers isArray', function() {
  it( 'should return true for arrays', function() {
    expect( typeCheckers.isArray( anArray ) ).to.be.true;
  } );

  it( 'should return false for objects', function() {
    expect( typeCheckers.isArray( anObject ) ).to.be.false;
  } );
} );

describe( 'TypeCheckers isFunction', function() {
  it( 'should return true for a functions', function() {
    expect( typeCheckers.isFunction( aFunction ) ).to.be.true;
  } );

  it( 'should return false for a non-function', function() {
    expect( typeCheckers.isFunction( aString ) ).to.be.false;
  } );
} );

describe( 'TypeCheckers isEmpty', function() {
  it( 'should return true for empty vars', function() {
    expect( typeCheckers.isEmpty( blankVar ) ).to.be.true;
  } );

  it( 'should return false for non-empty vars', function() {
    expect( typeCheckers.isEmpty( aString ) ).to.be.false;
  } );
} );
