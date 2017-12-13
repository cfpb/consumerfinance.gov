const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

const chai = require( 'chai' );
const expect = chai.expect;

const BaseTransition =
  require( BASE_JS_PATH + 'modules/transition/BaseTransition' );

const HTML_SNIPPET = '<div class="content-1"></div>' +
                     '<div class="content-2"></div>';

describe( 'BaseTransition', () => {

  let transition;

  // DOM-related settings.
  let document;
  let contentDom;
  let content2Dom;

  beforeEach( () => {
    this.jsdom = require( 'jsdom-global' )( HTML_SNIPPET );
    document = window.document;
    contentDom = document.querySelector( '.content-1' );
    content2Dom = document.querySelector( '.content-2' );
    transition =
      new BaseTransition( contentDom, { BASE_CLASS: 'u-test-transition' } );
  } );

  afterEach( () => this.jsdom() );

  describe( '.init()', () => {
    it( 'should have public static methods', () => {
      expect( BaseTransition.BEGIN_EVENT ).to.equal( 'transitionBegin' );
      expect( BaseTransition.END_EVENT ).to.equal( 'transitionEnd' );
      expect( BaseTransition.NO_ANIMATION_CLASS ).to.equal( 'u-no-animation' );
    } );

    it( 'should have correct state before initializing', () => {
      expect( transition.isAnimated() ).to.be.false;
      expect( transition.remove() ).to.be.false;
      expect( transition.animateOn() instanceof BaseTransition ).to.be.true;
      expect( transition.animateOff() instanceof BaseTransition ).to.be.true;
    } );

    it( 'should have correct state after initializing', () => {
      expect( transition.init() instanceof BaseTransition ).to.be.true;
    } );
  } );

  describe( '.setElement()', () => {
    it( 'should move classes from old element to new element', () => {
      const className = 'u-test-transition';
      expect( contentDom.classList.contains( className ) ).to.be.false;
      transition.init();
      expect( contentDom.classList.contains( className ) ).to.be.true;
      transition.setElement( content2Dom );
      expect( contentDom.classList.contains( className ) ).to.be.false;
      expect( content2Dom.classList.contains( className ) ).to.be.true;
    } );
  } );

  describe( '.halt()', () => {
    xit( 'should immediately fire transition end event', () => {

      /* TODO: To test halt() the transition needs to be started and
         then halt() needs to be called before the transition
         duration has completed. */
    } );
  } );

  describe( '.remove()', () => {
    it( 'should remove transition classes from element', () => {
      transition.init();
      let hasClass = contentDom.classList.contains( 'u-test-transition' );
      expect( hasClass ).to.be.true;
      expect( transition.remove() ).to.be.true;
      hasClass = contentDom.classList.contains( 'u-test-transition' );
      expect( hasClass ).to.be.false;
    } );
  } );

  describe( '.isAnimated()', () => {
    beforeEach( () => {
      transition.init();
    } );

    it( 'should be true after animation is initialized', () => {
      expect( transition.isAnimated() ).to.be.true;
    } );

    it( 'should be true after animation is turned On', () => {
      transition.animateOn();
      expect( transition.isAnimated() ).to.be.true;
    } );

    it( 'should be false after animation is turned Off', () => {
      transition.animateOff();
      expect( transition.isAnimated() ).to.be.false;
    } );
  } );

  describe( '.animateOff()', () => {
    beforeEach( () => {
      transition.init();
    } );

    it( 'should return an instance', () => {
      expect( transition.animateOff() instanceof BaseTransition ).to.be.true;
    } );

    it( 'should set u-no-animation class when called', () => {
      expect( contentDom.classList.contains( 'u-no-animation' ) ).to.be.false;
      transition.animateOff();
      expect( contentDom.classList.contains( 'u-no-animation' ) ).to.be.true;
    } );
  } );

  describe( '.animateOn()', () => {
    beforeEach( () => {
      transition.init();
    } );

    it( 'should return an instance', () => {
      expect( transition.animateOn() instanceof BaseTransition ).to.be.true;
    } );

    it( 'should remove u-no-animation class, if set', () => {
      transition.animateOff();
      transition.animateOn();
      expect( contentDom.classList.contains( 'u-no-animation' ) ).to.be.false;
    } );
  } );

  describe( '.applyClass()', () => {
    it( 'should apply a class', () => {
      expect( transition.applyClass( 'u-test-transition' ) ).to.be.false;
      transition.init();
      contentDom.classList.remove( 'u-test-transition' );
      expect( transition.applyClass( 'u-test-transition' ) ).to.be.true;
      expect( transition.applyClass( 'u-test-transition' ) ).to.be.false;
    } );
  } );
} );
