'use strict';
var BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';
var chai = require( 'chai' );
var expect = chai.expect;
var jsdom = require( 'mocha-jsdom' );
var sinon = require( 'sinon' );
var sandbox;

var behavior = require( BASE_JS_PATH + 'modules/util/behavior' );

function triggerEvent( target, eventType, eventOption ) {
  var event = document.createEvent( 'Event' );
  if ( eventType === 'keyup' ) {
    event.keyCode = eventOption || '';
  }
  event.initEvent( eventType, true, true );
  target.dispatchEvent( event );
}

describe( 'behavior', function() {
  jsdom();

  var HTML_SNIPPET =
  '<a href="#main" id="skip-nav">Skip to main content</a>' +
  '<a class="o-mega-menu_content-link o-mega-menu_content-1-link"' +
      'data-js-hook="behavior_flyout-menu_trigger">' +
        'Consumer Tools' +
  '</a>' +
  '<a class="o-mega-menu_content-link o-mega-menu_content-1-link"' +
      'data-js-hook="behavior_flyout-menu_trigger">' +
        'Educational Resources' +
  '</a>' +
  '<div data-js-hook="behavior_flyout-menu">' +
      '<div data-js-hook="behavior_flyout-menu_content"></div>' +
  '</div>';

  var containerDom;
  var behaviorElmDom;
  var selector = 'data-js-hook=behavior_flyout-menu';

  beforeEach( function() {
    sandbox = sinon.sandbox.create();
    document.body.innerHTML = HTML_SNIPPET;
    containerDom = document.querySelector( '[' + selector + ']' );
    behaviorElmDom = document.querySelector( '[' + selector + '_content]' );
  } );

  afterEach( function() {
    sandbox.restore();
  } );

  describe( 'attach function', function() {
    it( 'should register an event callback when passed a Node',
    function() {
      var spy = sinon.spy();
      var linkDom = document.querySelector( 'a[href^="#"]' );
      behavior.attach( linkDom, 'click', spy );
      triggerEvent( linkDom, 'click' );
      expect( spy.called ).to.equal( true );
    } );

    it( 'should register an event callback when passed a NodeList',
    function() {
      var spy = sinon.spy();
      var behaviorDom = behavior.find( 'flyout-menu_trigger' );
      behavior.attach( behaviorDom, 'mouseover', spy );
      triggerEvent( behaviorDom[0], 'mouseover' );
      expect( spy.called ).to.equal( true );
    } );

    it( 'should register an event callback when passed a behavior selector',
    function() {
      var spy = sinon.spy();
      var behaviorDom = behavior.find( 'flyout-menu_trigger' );
      behavior.attach( 'flyout-menu_trigger', 'mouseover', spy );
      triggerEvent( behaviorDom[0], 'mouseover' );
      expect( spy.called ).to.equal( true );
    } );

    it( 'should register an event callback when passed a dom selector',
    function() {
      var spy = sinon.spy();
      var linkDom = document.querySelector( 'a[href^="#"]' );
      behavior.attach( 'a[href^="#"]', 'click', spy );
      triggerEvent( linkDom, 'click' );
      expect( spy.called ).to.equal( true );
    } );
  } );

  describe( 'checkBehaviorDom function ', function() {
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

  describe( 'find function', function() {
    it( 'should find all elements with the specific behavior hook',
    function() {
      var behaviorDom = behavior.find( 'flyout-menu_trigger' );
      expect( behaviorDom.length === 2 ).to.equal( true );
      behaviorDom = behavior.find( 'flyout-menu_content' );
      expect( behaviorDom.length === 1 ).to.equal( true );
    } );

    it( 'should throw an error when passed an invalid behavior selector',
    function() {
      var behaviorSelector = 'a[href^="#"]';
      var errorMsg =
        '[data-js-hook*=behavior_' + behaviorSelector + '] not found in DOM!';
      var findFunction = behavior.find.bind( this, behaviorSelector );
      expect( findFunction ).to.throw( Error, errorMsg );
    } );
  } );

  describe( 'remove function', function() {
    it( 'should remove the event callback for the specific behavior hook',
    function() {
      var spy = sinon.spy();
      var linkDom = document.querySelector( 'a[href^="#"]' );
      behavior.attach( linkDom, 'click', spy );
      triggerEvent( linkDom, 'click' );
      expect( spy.called ).to.equal( true );
      spy.reset();
      behavior.remove( linkDom, 'click', spy );
      triggerEvent( linkDom, 'click' );
      expect( spy.called ).to.equal( false );
    } );
  } );
} );
