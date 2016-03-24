'use strict';
var chai = require( 'chai' );
var expect = chai.expect;
var sinon = require( 'sinon' );
var jsdom = require( 'mocha-jsdom' );
var BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';
var ERROR_MESSAGES = require( BASE_JS_PATH + 'config/error-messages-config' );
var domTraverse = require( BASE_JS_PATH + 'modules/util/dom-traverse' );

describe( 'Dom Traverse queryOne', function() {
  jsdom();

  before( function() {
    document.body.innerHTML =
      '<div class="div-1"></div><div class="query-2"></div>';
  } );

  it( 'should return the first elem if the expr is a string', function() {
    var query = domTraverse.queryOne( 'div' );

    expect( query.className ).to.equal( 'div-1' );
  } );

  it( 'should return the passed expr if it’s an object', function() {
    var obj = document.createElement( 'div' );
    obj.className = 'div-3';
    var query = domTraverse.queryOne( obj );

    expect( query.className ).to.equal( 'div-3' );
  } );

  it( 'should return null if the elem doesn’t exist', function() {
    var query = document.querySelector( '.div-4' );

    expect( query ).to.equal( null );
  } );
} );
