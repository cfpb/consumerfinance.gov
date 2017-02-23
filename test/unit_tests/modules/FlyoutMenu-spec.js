'use strict';

var BASE_JS_PATH = '../../../cfgov/unprocessed/js/';

var chai = require( 'chai' );
var expect = chai.expect;
var jsdom = require( 'jsdom' );
var sinon = require( 'sinon' );

var FlyoutMenu = require( BASE_JS_PATH + 'modules/behavior/FlyoutMenu' );
var MoveTransition =
  require( BASE_JS_PATH + 'modules/transition/MoveTransition' );

describe( 'FlyoutMenu', function() {

  var flyoutMenu;

  // Sinon-related settings.
  var triggerClickSpy;
  var triggerOverSpy;
  var expandBeginSpy;
  var expandEndSpy;
  var collapseBeginSpy;
  var collapseEndSpy;

  // DOM-related settings.
  var initdom;
  var window;
  var document;
  var HTML_SNIPPET =
    '<div data-js-hook="behavior_flyout-menu">' +
      '<button data-js-hook="behavior_flyout-menu_trigger" ' +
              'aria-pressed="false" ' +
              'aria-expanded="false"></button>' +
      '<div data-js-hook="behavior_flyout-menu_content" aria-expanded="false">' +
        '<button data-js-hook="behavior_flyout-menu_alt-trigger" ' +
                'aria-expanded="false"></button>' +
      '</div>' +
    '</div>';
  var SEL_PREFIX = '[data-js-hook=behavior_flyout-menu';

  var containerDom;
  var triggerDom;
  var contentDom;
  var altTriggerDom;

  beforeEach( function() {
    initdom = jsdom.jsdom( HTML_SNIPPET );
    window = initdom.defaultView;
    document = window.document;

    containerDom = document.querySelector( SEL_PREFIX + ']' );
    triggerDom =
      document.querySelector( SEL_PREFIX + '_trigger]' );
    contentDom =
      document.querySelector( SEL_PREFIX + '_content]' );
    // TODO: check for cases where alt trigger is absent.
    altTriggerDom =
      document.querySelector( SEL_PREFIX + '_alt-trigger]' );

    flyoutMenu = new FlyoutMenu( containerDom );
  } );

  describe( '.init()', function() {
    it( 'should have public static methods', function() {
      expect( FlyoutMenu.EXPAND_TYPE ).to.equal( 'expand' );
      expect( FlyoutMenu.COLLAPSE_TYPE ).to.equal( 'collapse' );
      expect( FlyoutMenu.BASE_CLASS ).to.equal( 'behavior_flyout-menu' );
    } );

    it( 'should have correct state before initializing', function() {
      expect( triggerDom.getAttribute( 'aria-pressed' ) ).to.equal( 'false' );
      expect( triggerDom.getAttribute( 'aria-expanded' ) ).to.equal( 'false' );
      expect( contentDom.getAttribute( 'aria-expanded' ) ).to.equal( 'false' );
      expect( altTriggerDom.getAttribute( 'aria-pressed' ) ).to.be.null;
      expect( altTriggerDom.getAttribute( 'aria-expanded' ) ).to.equal( 'false' );

      expect( flyoutMenu.isAnimating() ).to.be.false;
      expect( flyoutMenu.isExpanded() ).to.be.false;
      expect( flyoutMenu.getTransition() ).to.be.undefined;
      expect( flyoutMenu.getData() ).to.be.undefined;
    } );

    it( 'should have correct state after initializing', function() {
      expect( flyoutMenu.init() instanceof FlyoutMenu ).to.be.true;
    } );
  } );

  describe( 'mouseover/click', function() {
    beforeEach( function() {
      // Set up expected event listeners.
      triggerOverSpy = sinon.spy();
      triggerClickSpy = sinon.spy();

      flyoutMenu.init();
      flyoutMenu.addEventListener( 'triggerOver', triggerOverSpy );
      flyoutMenu.addEventListener( 'triggerClick', triggerClickSpy );
    } );

    afterEach( function() {
      // Check expected event broadcasts.
      expect( triggerOverSpy.callCount ).to.equal( 1 );
      var args = triggerOverSpy.getCall( 0 ).args[0];
      expect( args.target ).to.equal( flyoutMenu );
      expect( args.type ).to.equal( 'triggerOver' );

      expect( triggerClickSpy.callCount ).to.equal( 1 );
      args = triggerClickSpy.getCall( 0 ).args[0];
      expect( args.target ).to.equal( flyoutMenu );
      expect( args.type ).to.equal( 'triggerClick' );
    } );

    it( 'should dispatch events when called by trigger click', function() {
      // TODO: Ideally this would use `new MouseEvent`,
      //       but how do we import MouseEvent (or Event) into Mocha.
      //       Please investigate.
      var mouseEvent = document.createEvent( 'MouseEvents' );
      mouseEvent.initEvent( 'mouseover', true, true );
      triggerDom.dispatchEvent( mouseEvent );
      triggerDom.click();
    } );

    xit( 'should dispatch events when called by alt trigger click', function() {
      // TODO: alt trigger doesn't dispatch mouseover events,
      //       but it probably should to match the trigger API.
      var mouseEvent = document.createEvent( 'MouseEvents' );
      mouseEvent.initEvent( 'mouseover', true, true );
      altTriggerDom.dispatchEvent( mouseEvent );
      altTriggerDom.click();
    } );
  } );

  describe( '.expand()', function() {
    beforeEach( function() {
      // Set up expected event listeners.
      expandBeginSpy = sinon.spy();
      expandEndSpy = sinon.spy();

      flyoutMenu.init();
      flyoutMenu.addEventListener( 'expandBegin', expandBeginSpy );
      flyoutMenu.addEventListener( 'expandEnd', expandEndSpy );
    } );

    afterEach( function() {
      // Check expected event broadcasts.
      expect( expandBeginSpy.callCount ).to.equal( 1 );
      var args = expandBeginSpy.getCall( 0 ).args[0];
      expect( args.target ).to.equal( flyoutMenu );
      expect( args.type ).to.equal( 'expandBegin' );

      expect( expandEndSpy.callCount ).to.equal( 1 );
      args = expandEndSpy.getCall( 0 ).args[0];
      expect( args.target ).to.equal( flyoutMenu );
      expect( args.type ).to.equal( 'expandEnd' );

      // Check expected aria attributes state.
      expect( triggerDom.getAttribute( 'aria-pressed' ) ).to.equal( 'true' );
      expect( triggerDom.getAttribute( 'aria-expanded' ) ).to.equal( 'true' );
      expect( contentDom.getAttribute( 'aria-expanded' ) ).to.equal( 'true' );
      expect( altTriggerDom.getAttribute( 'aria-pressed' ) ).to.be.null;
      expect( altTriggerDom.getAttribute( 'aria-expanded' ) )
        .to.equal( 'true' );
    } );

    it( 'should dispatch events and set aria attributes, ' +
        'when called by trigger click', function() {
      triggerDom.click();
    } );

    it( 'should dispatch events and set aria attributes, ' +
        'when called by alt trigger click', function() {
      altTriggerDom.click();
    } );

    it( 'should dispatch events and set aria attributes, ' +
        'when called directly', function() {
      flyoutMenu.expand();
    } );
  } );

  describe( '.collapse()', function() {
    beforeEach( function() {
      // Set up expected event listeners.
      collapseBeginSpy = sinon.spy();
      collapseEndSpy = sinon.spy();

      flyoutMenu.init();
      flyoutMenu.addEventListener( 'collapseBegin', collapseBeginSpy );
      flyoutMenu.addEventListener( 'collapseEnd', collapseEndSpy );
      triggerDom.click();
    } );

    afterEach( function() {
      // Check expected event broadcasts.
      expect( collapseBeginSpy.callCount ).to.equal( 1 );
      var args = collapseBeginSpy.getCall( 0 ).args[0];
      expect( args.target ).to.equal( flyoutMenu );
      expect( args.type ).to.equal( 'collapseBegin' );

      expect( collapseEndSpy.callCount ).to.equal( 1 );
      args = collapseEndSpy.getCall( 0 ).args[0];
      expect( args.target ).to.equal( flyoutMenu );
      expect( args.type ).to.equal( 'collapseEnd' );

      // Check expected aria attribute states.
      expect( triggerDom.getAttribute( 'aria-pressed' ) ).to.equal( 'false' );
      expect( triggerDom.getAttribute( 'aria-expanded' ) ).to.equal( 'false' );
      expect( contentDom.getAttribute( 'aria-expanded' ) ).to.equal( 'false' );
      expect( altTriggerDom.getAttribute( 'aria-pressed' ) ).to.be.null;
      expect( altTriggerDom.getAttribute( 'aria-expanded' ) )
        .to.equal( 'false' );
    } );

    it( 'should dispatch events and set aria attributes, ' +
        'when called by trigger click', function() {
      triggerDom.click();
    } );

    it( 'should dispatch events and set aria attributes, ' +
        'when called by alt trigger click', function() {
      altTriggerDom.click();
    } );

    it( 'should dispatch events and set aria attributes, ' +
        'when called directly', function() {
      flyoutMenu.collapse();
    } );
  } );

  describe( '.setExpandTransition()', function() {
    it( 'should set a transition', function( done ) {
      flyoutMenu.init();
      var transition = new MoveTransition( contentDom ).init();
      flyoutMenu.setExpandTransition( transition, transition.moveLeft );
      flyoutMenu.addEventListener( 'expandEnd', function() {
        try {
          var hasClass = contentDom.classList.contains( 'u-move-transition' );
          expect( hasClass ).to.be.true;
          done();
        } catch ( err ) {
          done( err );
        }
      } );
      triggerDom.click();
    } );
  } );

  describe( '.setCollapseTransition()', function() {
    it( 'should set a transition', function( done ) {
      flyoutMenu.init();
      var transition = new MoveTransition( contentDom ).init();
      triggerDom.click();
      flyoutMenu.setCollapseTransition( transition, transition.moveLeft );
      flyoutMenu.addEventListener( 'collapseEnd', function() {
        try {
          var hasClass = contentDom.classList.contains( 'u-move-transition' );
          expect( hasClass ).to.be.true;
          done();
        } catch ( err ) {
          done( err );
        }
      } );
      triggerDom.click();
    } );
  } );

  describe( '.getTransition()', function() {
    it( 'should return a transition instance', function() {
      flyoutMenu.init();
      expect( flyoutMenu.getTransition() ).to.be.undefined;
      var transition = new MoveTransition( contentDom ).init();
      flyoutMenu.setExpandTransition( transition, transition.moveLeft );
      flyoutMenu.setCollapseTransition( transition, transition.moveToOrigin );
      expect( flyoutMenu.getTransition() ).to.equal( transition );
      expect( flyoutMenu.getTransition( FlyoutMenu.COLLAPSE_TYPE ) )
        .to.equal( transition );
    } );
  } );

  describe( '.clearTransitions()', function() {
    it( 'should remove all transitions', function() {
      flyoutMenu.init();
      var transition = new MoveTransition( contentDom ).init();
      flyoutMenu.setExpandTransition( transition, transition.moveLeft );
      flyoutMenu.setCollapseTransition( transition, transition.moveToOrigin );
      var hasClass = contentDom.classList.contains( 'u-move-transition' );
      expect( hasClass ).to.be.true;
      flyoutMenu.clearTransitions();
      expect( flyoutMenu.getTransition() ).to.be.undefined;
      hasClass = contentDom.classList.contains( 'u-move-transition' );
      expect( hasClass ).to.be.false;
    } );
  } );

  describe( '.getDom()', function() {
    it( 'should return references to full dom', function() {
      flyoutMenu.init();
      var dom = flyoutMenu.getDom();
      expect( dom.container ).to.equal( containerDom );
      expect( dom.trigger ).to.equal( triggerDom );
      expect( dom.content ).to.equal( contentDom );
      expect( dom.altTrigger ).to.equal( altTriggerDom );
    } );
  } );

  describe( 'suspend/resume behavior', function() {
    beforeEach( function() {
      // Set up expected event listeners.
      expandBeginSpy = sinon.spy();
      expandEndSpy = sinon.spy();
      collapseBeginSpy = sinon.spy();
      collapseEndSpy = sinon.spy();
      flyoutMenu.init();
      flyoutMenu.addEventListener( 'expandBegin', expandBeginSpy );
      flyoutMenu.addEventListener( 'expandEnd', expandEndSpy );
      flyoutMenu.addEventListener( 'collapseBegin', collapseBeginSpy );
      flyoutMenu.addEventListener( 'collapseEnd', collapseEndSpy );
    } );

    describe( '.suspend()', function() {
      it( 'should not broadcast events after being suspended', function() {
        // Set up expected event listeners.
        flyoutMenu.suspend();
        triggerDom.click();
        expect( expandBeginSpy.callCount ).to.equal( 0 );
        expect( expandEndSpy.callCount ).to.equal( 0 );
        expect( collapseBeginSpy.callCount ).to.equal( 0 );
        expect( collapseEndSpy.callCount ).to.equal( 0 );
      } );
    } );

    describe( '.resume()', function() {
      it( 'should broadcast events after resuming from suspended', function() {
        // Set up expected event listeners.
        flyoutMenu.suspend();
        flyoutMenu.resume();
        triggerDom.click();
        expect( expandBeginSpy.callCount ).to.equal( 1 );
        expect( expandEndSpy.callCount ).to.equal( 1 );
        triggerDom.click();
        expect( collapseBeginSpy.callCount ).to.equal( 1 );
        expect( collapseEndSpy.callCount ).to.equal( 1 );
      } );
    } );

  } );

  describe( '.setData()', function() {
    it( 'should return the instance when set', function() {
      flyoutMenu.init();
      var inst = flyoutMenu.setData( 'test-data' );
      expect( inst instanceof FlyoutMenu ).to.be.true;
    } );
  } );

  describe( '.getData()', function() {
    it( 'should return the set data', function() {
      flyoutMenu.init();
      flyoutMenu.setData( 'test-data' );
      expect( flyoutMenu.getData() ).to.equal( 'test-data' );
    } );
  } );

  describe( '.isAnimating()', function() {
    it( 'should return true when expanding', function( done ) {
      flyoutMenu.init();
      flyoutMenu.addEventListener( 'expandBegin', function() {
        try {
          expect( flyoutMenu.isAnimating() ).to.be.true;
          done();
        } catch ( err ) {
          done( err );
        }
      } );
      triggerDom.click();
    } );

    it( 'should return false after expanding', function( done ) {
      flyoutMenu.init();
      flyoutMenu.addEventListener( 'expandEnd', function() {
        try {
          expect( flyoutMenu.isAnimating() ).to.be.false;
          done();
        } catch ( err ) {
          done( err );
        }
      } );
      triggerDom.click();
    } );

    it( 'should return true while collapsing', function( done ) {
      flyoutMenu.init();
      flyoutMenu.addEventListener( 'collapseBegin', function() {
        try {
          expect( flyoutMenu.isAnimating() ).to.be.true;
          done();
        } catch ( err ) {
          done( err );
        }
      } );
      triggerDom.click();
      triggerDom.click();
    } );

    it( 'should return false after collapsing', function( done ) {
      flyoutMenu.init();
      flyoutMenu.addEventListener( 'collapseEnd', function() {
        try {
          expect( flyoutMenu.isAnimating() ).to.be.false;
          done();
        } catch ( err ) {
          done( err );
        }
      } );
      triggerDom.click();
      triggerDom.click();
    } );
  } );

  describe( '.isExpanded()', function() {
    it( 'should return false before expanding', function( done ) {
      flyoutMenu.init();
      flyoutMenu.addEventListener( 'expandBegin', function() {
        try {
          expect( flyoutMenu.isExpanded() ).to.be.false;
          done();
        } catch ( err ) {
          done( err );
        }
      } );
      triggerDom.click();
    } );

    it( 'should return true after expanding', function( done ) {
      flyoutMenu.init();
      flyoutMenu.addEventListener( 'expandEnd', function() {
        try {
          expect( flyoutMenu.isExpanded() ).to.be.true;
          done();
        } catch ( err ) {
          done( err );
        }
      } );
      triggerDom.click();
    } );

    it( 'should return true before collapsing', function( done ) {
      flyoutMenu.init();
      triggerDom.click();
      flyoutMenu.addEventListener( 'triggerClick', function() {
        try {
          expect( flyoutMenu.isExpanded() ).to.be.true;
          done();
        } catch ( err ) {
          done( err );
        }
      } );
      triggerDom.click();
    } );

    it( 'should return false after collapsing', function( done ) {
      flyoutMenu.init();
      flyoutMenu.addEventListener( 'collapseEnd', function() {
        try {
          expect( flyoutMenu.isExpanded() ).to.be.false;
          done();
        } catch ( err ) {
          done( err );
        }
      } );
      triggerDom.click();
      triggerDom.click();
    } );
  } );
} );
