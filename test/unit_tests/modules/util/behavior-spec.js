'use strict';

var BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

var chai = require( 'chai' );
var expect = chai.expect;
var jsdom = require( 'jsdom' );

var behavior = require( BASE_JS_PATH + 'modules/util/behavior' );

describe( 'behavior', function() {

  var HTML_SNIPPET = '<div data-js-hook="behavior_flyout-menu">' +
                     '<div data-js-hook="behavior_flyout-menu_content">' +
                     '</div></div>';
  var initdom = jsdom.jsdom( HTML_SNIPPET );
  var document = initdom.defaultView.document;

  var containerDom;
  var behaviorElmDom;
  var selector = 'data-js-hook=behavior_flyout-menu';

  before( function() {
    containerDom = document.querySelector( '[' + selector + ']' );
    behaviorElmDom = document.querySelector( '[' + selector + '_content]' );
  } );

  describe( '.checkBehaviorDom()', function() {
    it( 'should throw an error if element DOM not found', function() {
      var errMsg = 'behavior_flyout-menu ' +
                   'behavior not found on passed DOM node!';
      function errFunc() {
        behavior.checkBehaviorDom( null, 'behavior_flyout-menu' );
      }
      expect( errFunc ).to.throw( Error, errMsg );
    } );

    it( 'should throw an error if behavior attribute not found', function() {
      var errMsg = 'mock-attr behavior not found on passed DOM node!';
      function errFunc() {
        behavior.checkBehaviorDom( containerDom, 'mock-attr' );
      }
      expect( errFunc ).to.throw( Error, errMsg );
    } );

    it( 'should return the correct HTMLElement ' +
        'when direct element is searched', function() {
      var dom = behavior.checkBehaviorDom( containerDom,
                                           'behavior_flyout-menu' );
      expect( dom ).to.be.equal( containerDom );
    } );

    it( 'should return the correct HTMLElement ' +
        'when child element is searched', function() {
      var dom = behavior.checkBehaviorDom( behaviorElmDom,
                                           'behavior_flyout-menu_content' );
      expect( dom ).to.be.equal( behaviorElmDom );
    } );
  } );
} );
