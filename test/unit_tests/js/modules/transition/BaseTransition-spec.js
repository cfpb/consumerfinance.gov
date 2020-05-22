import BaseTransition from '../../../../../cfgov/unprocessed/js/modules/transition/BaseTransition';

let transition;

// DOM-related settings.
let contentDom;
let content2Dom;

const HTML_SNIPPET = '<div class="content-1"></div>' +
                     '<div class="content-2"></div>';

describe( 'BaseTransition', () => {
  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
    contentDom = document.querySelector( '.content-1' );
    content2Dom = document.querySelector( '.content-2' );
    transition =
      new BaseTransition( contentDom, { BASE_CLASS: 'u-test-transition' } );
  } );

  describe( '.init()', () => {
    it( 'should have public static methods', () => {
      expect( BaseTransition.BEGIN_EVENT ).toStrictEqual( 'transitionBegin' );
      expect( BaseTransition.END_EVENT ).toStrictEqual( 'transitionEnd' );
      expect( BaseTransition.NO_ANIMATION_CLASS ).toStrictEqual( 'u-no-animation' );
    } );

    it( 'should have correct state before initializing', () => {
      expect( transition.isAnimated() ).toBe( false );
      expect( transition.remove() ).toBe( false );
      expect( transition.animateOn() instanceof BaseTransition ).toBe( true );
      expect( transition.animateOff() instanceof BaseTransition ).toBe( true );
    } );

    it( 'should have correct state after initializing', () => {
      expect( transition.init() instanceof BaseTransition ).toBe( true );
    } );
  } );

  describe( '.setElement()', () => {
    it( 'should move classes from old element to new element', () => {
      const className = 'u-test-transition';
      expect( contentDom.classList.contains( className ) ).toBe( false );
      transition.init();
      expect( contentDom.classList.contains( className ) ).toBe( true );
      transition.setElement( content2Dom );
      expect( contentDom.classList.contains( className ) ).toBe( false );
      expect( content2Dom.classList.contains( className ) ).toBe( true );
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
      expect( hasClass ).toBe( true );
      expect( transition.remove() ).toBe( true );
      hasClass = contentDom.classList.contains( 'u-test-transition' );
      expect( hasClass ).toBe( false );
    } );
  } );

  describe( '.isAnimated()', () => {
    beforeEach( () => {
      transition.init();
    } );

    it( 'should be true after animation is initialized', () => {
      expect( transition.isAnimated() ).toBe( true );
    } );

    it( 'should be true after animation is turned On', () => {
      transition.animateOn();
      expect( transition.isAnimated() ).toBe( true );
    } );

    it( 'should be false after animation is turned Off', () => {
      transition.animateOff();
      expect( transition.isAnimated() ).toBe( false );
    } );
  } );

  describe( '.animateOff()', () => {
    beforeEach( () => {
      transition.init();
    } );

    it( 'should return an instance', () => {
      expect( transition.animateOff() instanceof BaseTransition ).toBe( true );
    } );

    it( 'should set u-no-animation class when called', () => {
      expect( contentDom.classList.contains( 'u-no-animation' ) ).toBe( false );
      transition.animateOff();
      expect( contentDom.classList.contains( 'u-no-animation' ) ).toBe( true );
    } );
  } );

  describe( '.animateOn()', () => {
    beforeEach( () => {
      transition.init();
    } );

    it( 'should return an instance', () => {
      expect( transition.animateOn() instanceof BaseTransition ).toBe( true );
    } );

    it( 'should remove u-no-animation class, if set', () => {
      transition.animateOff();
      transition.animateOn();
      expect( contentDom.classList.contains( 'u-no-animation' ) ).toBe( false );
    } );
  } );

  describe( '.applyClass()', () => {
    it( 'should apply a class', () => {
      expect( transition.applyClass( 'u-test-transition' ) ).toBe( false );
      transition.init();
      contentDom.classList.remove( 'u-test-transition' );
      expect( transition.applyClass( 'u-test-transition' ) ).toBe( true );
      expect( transition.applyClass( 'u-test-transition' ) ).toBe( false );
    } );
  } );
} );
