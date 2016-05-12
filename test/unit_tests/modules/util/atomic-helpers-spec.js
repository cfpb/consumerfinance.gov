'use strict';

var BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

var chai = require( 'chai' );
var expect = chai.expect;
var jsdom = require( 'jsdom' );

var atomicHelpers = require( BASE_JS_PATH + 'modules/util/atomic-helpers' );

describe( 'atomic-helpers', function() {

  var HTML_SNIPPET = '<div class="container">' +
                     '<div class="m-expandable"></div></div>';
  var initdom = jsdom.jsdom( HTML_SNIPPET );
  var document = initdom.defaultView.document;

  var containerDom;
  var expandableDom;

  before( function() {
    containerDom = document.querySelector( '.container' );
    expandableDom = document.querySelector( '.m-expandable' );
  } );

  describe( '.checkDom()', function() {
    it( 'should throw an error if element DOM not found', function() {
      var errMsg = 'null passed to Expandable.js is not valid. ' +
                   'Check that element is a valid DOM node';
      function errFunc() {
        atomicHelpers.checkDom( null, '.m-expandable', 'Expandable' );
      }
      expect( errFunc ).to.throw( Error, errMsg );
    } );

    it( 'should throw an error if element class not found', function() {
      var errMsg = 'mock-class not found on or in passed DOM node.';
      function errFunc() {
        atomicHelpers.checkDom( expandableDom, 'mock-class', 'Expandable' );
      }
      expect( errFunc ).to.throw( Error, errMsg );
    } );

    it( 'should return the correct HTMLElement ' +
        'when direct element is searched', function() {
      var dom =
        atomicHelpers.checkDom( expandableDom, 'm-expandable', 'Expandable' );
      expect( dom ).to.be.equal( expandableDom );
    } );

    it( 'should return the correct HTMLElement ' +
        'when parent element is searched', function() {
      var dom =
        atomicHelpers.checkDom( containerDom, 'm-expandable', 'Expandable' );
      expect( dom ).to.be.equal( expandableDom );
    } );
  } );

  describe( '.instantiateAll()', function() {
    xit( 'should return an array of instances', function() {
      // TODO: Implement test.
    } );
  } );

  describe( '.setInitFlag()', function() {
    xit( 'should return true when init flag is set', function() {
      // TODO: Implement test.
    } );

    xit( 'should return false when init flag is already set', function() {
      // TODO: Implement test.
    } );
  } );
} );
