'use strict';

var BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

var chai = require( 'chai' );
var expect = chai.expect;
var jsdom = require( 'jsdom' );

var atomicHelpers = require( BASE_JS_PATH + 'modules/util/atomic-helpers' );

describe( 'atomic-helpers', function() {

  var containerDom;
  var expandableDom;
  var initdom = jsdom.jsdom( '<div class="container"><div class="m-expandable"></div></div>' );
  var document = initdom.defaultView.document;

  before( function() {
    containerDom = document.querySelector( '.container' );
    expandableDom = document.querySelector( '.m-expandable' );
  } );

  describe( '.checkDom()', function() {
    it( 'should throw an error if element DOM not found', function() {
      var errMsg = 'undefined passed to Expandable.js is not valid. ' +
                   'Check that element is a valid DOM node';
      var errFunc = function() {
        atomicHelpers.checkDom( undefined, '.m-expandable', 'Expandable' );
      };
      expect( errFunc ).to.throw( Error, errMsg );
    } );

    it( 'should throw an error if element class not found', function() {
      var errMsg = 'mock-class not found on or in passed DOM node.';
      var errFunc = function() {
        atomicHelpers.checkDom( expandableDom, 'mock-class', 'Expandable' );
      };
      expect( errFunc ).to.throw( Error, errMsg );
    } );

    it( 'should return the correct HTMLElement when direct element is searched', function() {
      var dom = atomicHelpers.checkDom( expandableDom, 'm-expandable', 'Expandable' );
      expect( dom ).to.be.equal( expandableDom );
    } );

    it( 'should return the correct HTMLElement when parent element is searched', function() {
      var dom = atomicHelpers.checkDom( containerDom, 'm-expandable', 'Expandable' );
      expect( dom ).to.be.equal( expandableDom );
    } );
  } );
} );
