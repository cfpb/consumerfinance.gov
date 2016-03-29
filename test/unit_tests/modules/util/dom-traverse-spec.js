'use strict';

var BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

var chai = require( 'chai' );
var expect = chai.expect;
var jsdom = require( 'mocha-jsdom' );
var domTraverse = require( BASE_JS_PATH + 'modules/util/dom-traverse' );

describe( 'Dom Traverse queryOne()', function() {
  jsdom();

  before( function() {
    document.body.innerHTML =
      '<div class="div-1"></div><div class="div-2"></div>';
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

describe( 'Dom Traverse getSiblings()', function() {
  jsdom();

  before( function() {
    document.body.innerHTML =
      '<div class="div-1"></div><div class="div-2"></div>';
  } );

  it( 'should return an array with a single sibling',
    function() {
      var elem = document.querySelector( '.div-1' );
      var siblings = domTraverse.getSiblings( elem, 'div' );

      expect( siblings.length ).to.equal( 1 );
      expect( siblings[0].className ).to.equal( 'div-2' );
    }
  );
} );

describe( 'Dom Traverse not()', function() {
  jsdom();

  before( function() {
    document.body.innerHTML =
      '<div class="div-1"></div><div class="div-2"></div>';
  } );

  it( 'should return an array with the item that wasn’t excluded',
    function() {
      var items = document.querySelectorAll( 'div' );
      var exclude = document.querySelector( '.div-2' );

      items = domTraverse.not( items, exclude );

      expect( items.length ).to.equal( 1 );
      expect( items[0].className ).to.equal( 'div-1' );
    }
  );
} );

describe( 'Dom Traverse closest()', function() {
  jsdom();

  before( function() {
    document.body.innerHTML =
      '<div class="grandparent"><div class="parent"><div class="child">' +
      '</div></div></div>';
  } );

  it( 'should return the immediate parent HTMLNode with a passed selector',
    function() {
      var child = document.querySelector( '.child' );
      var parent = domTraverse.closest( child, 'div' );

      expect( parent.className ).to.equal( 'parent' );
    }
  );

  it( 'should return the grandparent HTMLNode with a passed selector',
    function() {
      var child = document.querySelector( '.child' );
      var parent = domTraverse.closest( child, '.grandparent' );

      expect( parent.className ).to.equal( 'grandparent' );
    }
  );

  it( 'should return null without a passed selector',
    function() {
      var child = document.querySelector( '.child' );
      var parent = domTraverse.closest( child );

      expect( parent ).to.equal( null );
    }
  );

  it( 'should return the parent HTMLNode even if the selector wasn’t found',
    function() {
      var child = document.querySelector( '.child' );
      var parent = domTraverse.closest( child, 'greatgrandparent' );

      expect( parent ).to.equal( null );
    }
  );
} );
