'use strict';

var BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

var chai = require( 'chai' );
var expect = chai.expect;
var jsdom = require( 'jsdom' );

var BaseTransition =
  require( BASE_JS_PATH + 'modules/transition/BaseTransition' );

describe( 'BaseTransition', function() {

  var transition;

  // DOM-related settings.
  var initdom;
  var document;
  var HTML_SNIPPET = '<div class="content-1"></div>' +
                     '<div class="content-2"></div>';
  var contentDom;
  var content2Dom;

  beforeEach( function() {
    initdom = jsdom.jsdom( HTML_SNIPPET );
    document = initdom.defaultView.document;
    contentDom = document.querySelector( '.content-1' );
    content2Dom = document.querySelector( '.content-2' );
    transition =
      new BaseTransition( contentDom, { BASE_CLASS: 'u-test-transition' } );
  } );

  describe( '.init()', function() {
    it( 'should have public static methods', function() {
      expect( BaseTransition.BEGIN_EVENT ).to.equal( 'transitionBegin' );
      expect( BaseTransition.END_EVENT ).to.equal( 'transitionEnd' );
      expect( BaseTransition.NO_ANIMATION_CLASS ).to.equal( 'u-no-animation' );
    } );

    it( 'should have correct state before initializing', function() {
      expect( transition.isAnimated() ).to.be.false;
      expect( transition.remove() ).to.be.false;
      expect( transition.animateOn() instanceof BaseTransition ).to.be.true;
      expect( transition.animateOff() instanceof BaseTransition ).to.be.true;
    } );

    it( 'should have correct state after initializing', function() {
      expect( transition.init() instanceof BaseTransition ).to.be.true;
    } );
  } );

  describe( '.setElement()', function() {
    it( 'should move classes from old element to new element', function() {
      var className = 'u-test-transition';
      expect( contentDom.classList.contains( className ) ).to.be.false;
      transition.init();
      expect( contentDom.classList.contains( className ) ).to.be.true;
      transition.setElement( content2Dom );
      expect( contentDom.classList.contains( className ) ).to.be.false;
      expect( content2Dom.classList.contains( className ) ).to.be.true;
    } );
  } );

  describe( '.halt()', function() {
    xit( 'should immediately fire transition end event', function() {
      // TODO: To test halt() the transition needs to be started and
      //       then halt() needs to be called before the transition
      //       duration has completed.
    } );
  } );

  describe( '.remove()', function() {
    it( 'should remove transition classes from element', function() {
      transition.init();
      var hasClass = contentDom.classList.contains( 'u-test-transition' );
      expect( hasClass ).to.be.true;
      expect( transition.remove() ).to.be.true;
      hasClass = contentDom.classList.contains( 'u-test-transition' );
      expect( hasClass ).to.be.false;
    } );
  } );

  describe( '.isAnimated()', function() {
    beforeEach( function() {
      transition.init();
    } );

    it( 'should be true after animation is initialized', function() {
      expect( transition.isAnimated() ).to.be.true;
    } );

    it( 'should be true after animation is turned On', function() {
      transition.animateOn();
      expect( transition.isAnimated() ).to.be.true;
    } );

    it( 'should be false after animation is turned Off', function() {
      transition.animateOff();
      expect( transition.isAnimated() ).to.be.false;
    } );
  } );

  describe( '.animateOff()', function() {
    beforeEach( function() {
      transition.init();
    } );

    it( 'should return an instance', function() {
      expect( transition.animateOff() instanceof BaseTransition ).to.be.true;
    } );

    it( 'should set u-no-animation class when called', function() {
      expect( contentDom.classList.contains( 'u-no-animation' ) ).to.be.false;
      transition.animateOff();
      expect( contentDom.classList.contains( 'u-no-animation' ) ).to.be.true;
    } );
  } );

  describe( '.animateOn()', function() {
    beforeEach( function() {
      transition.init();
    } );

    it( 'should return an instance', function() {
      expect( transition.animateOn() instanceof BaseTransition ).to.be.true;
    } );

    it( 'should remove u-no-animation class, if set', function() {
      transition.animateOff();
      transition.animateOn();
      expect( contentDom.classList.contains( 'u-no-animation' ) ).to.be.false;
    } );
  } );

  describe( '.applyClass()', function() {
    it( 'should apply a class', function() {
      expect( transition.applyClass( 'u-test-transition' ) ).to.be.false;
      transition.init();
      contentDom.classList.remove( 'u-test-transition' );
      expect( transition.applyClass( 'u-test-transition' ) ).to.be.true;
      expect( transition.applyClass( 'u-test-transition' ) ).to.be.false;
    } );
  } );
} );
