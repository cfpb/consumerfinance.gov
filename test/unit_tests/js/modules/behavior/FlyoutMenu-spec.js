import FlyoutMenu from '../../../../../cfgov/unprocessed/js/modules/behavior/FlyoutMenu.js';
import MoveTransition from '@cfpb/cfpb-atomic-component/src/utilities/transition/MoveTransition';

const HTML_SNIPPET = `
<div data-js-hook="behavior_flyout-menu">
    <button data-js-hook="behavior_flyout-menu_trigger"
            aria-haspopup="menu"
            aria-expanded="false"></button>
    <div data-js-hook="behavior_flyout-menu_content" aria-expanded="false">
      <button data-js-hook="behavior_flyout-menu_trigger"
              aria-expanded="false"></button>
    </div>
</div>
`;

describe( 'FlyoutMenu', () => {

  let flyoutMenu;

  // Mock-related settings.
  let triggerClickSpy;
  let triggerOverSpy;
  let expandBeginSpy;
  let expandEndSpy;
  let collapseBeginSpy;
  let collapseEndSpy;

  // DOM-related settings.
  const SEL_PREFIX = '[data-js-hook=behavior_flyout-menu';

  let containerDom;
  let triggerDom;
  let contentDom;
  let altTriggerDom;

  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
    containerDom = document.querySelector( SEL_PREFIX + ']' );
    const triggersDom = document.querySelectorAll( SEL_PREFIX + '_trigger]' );
    triggerDom = triggersDom[0];
    contentDom = document.querySelector( SEL_PREFIX + '_content]' );
    // TODO: check for cases where alt trigger is absent.
    altTriggerDom = triggersDom[1];

    flyoutMenu = new FlyoutMenu( containerDom );
  } );

  describe( '.init()', () => {
    it( 'should have public static methods', () => {
      expect( FlyoutMenu.EXPAND_TYPE ).toBe( 'expand' );
      expect( FlyoutMenu.COLLAPSE_TYPE ).toBe( 'collapse' );
      expect( FlyoutMenu.BASE_CLASS ).toBe( 'behavior_flyout-menu' );
    } );

    it( 'should have correct state before initializing', () => {
      expect( triggerDom.getAttribute( 'aria-expanded' ) ).toBe( 'false' );
      expect( contentDom.getAttribute( 'aria-expanded' ) ).toBe( 'false' );
      expect(
        altTriggerDom.getAttribute( 'aria-expanded' )
      ).toBe( 'false' );

      expect( flyoutMenu.isAnimating() ).toBe( false );
      expect( flyoutMenu.isExpanded() ).toBe( false );
      expect( flyoutMenu.getTransition() ).toBeUndefined();
      expect( flyoutMenu.getData() ).toBeUndefined();
    } );

    it( 'should have correct state after initializing as collapsed', () => {
      expect( flyoutMenu.init() ).toBeInstanceOf( FlyoutMenu );
      expect( triggerDom.getAttribute( 'aria-expanded' ) ).toBe( 'false' );
      expect( contentDom.getAttribute( 'aria-expanded' ) ).toBe( 'false' );
    } );

    it( 'should have correct state after initializing as expanded', () => {
      expect( flyoutMenu.init( true ) ).toBeInstanceOf( FlyoutMenu );
      expect( triggerDom.getAttribute( 'aria-expanded' ) ).toBe( 'true' );
      expect( contentDom.getAttribute( 'aria-expanded' ) ).toBe( 'true' );
    } );
  } );

  describe( 'mouseover/click', () => {
    beforeEach( () => {
      // Set up expected event listeners.
      triggerOverSpy = jest.fn();
      triggerClickSpy = jest.fn();

      flyoutMenu.init();
      flyoutMenu.addEventListener( 'triggerOver', triggerOverSpy );
      flyoutMenu.addEventListener( 'triggerClick', triggerClickSpy );
    } );

    afterEach( () => {
      // Check expected event broadcasts.
      expect( triggerOverSpy ).toHaveBeenCalledTimes( 1 );
      expect( triggerOverSpy ).toHaveBeenCalledWith(
        { target: flyoutMenu, type: 'triggerOver' }
      );

      expect( triggerClickSpy ).toHaveBeenCalledTimes( 1 );
      expect( triggerClickSpy ).toHaveBeenCalledWith(
        { target: flyoutMenu, type: 'triggerClick' }
      );
    } );

    it( 'should dispatch events when called by trigger click', () => {

      /* TODO: Ideally this would use `new MouseEvent`,
         but how do we import MouseEvent (or Event) into Jest.
         Please investigate. */
      const mouseEvent = document.createEvent( 'MouseEvents' );
      mouseEvent.initEvent( 'mouseover', true, true );
      triggerDom.dispatchEvent( mouseEvent );
      triggerDom.click();
    } );

    it( 'should dispatch events when called by alt trigger click', () => {
      const mouseEvent = document.createEvent( 'MouseEvents' );
      mouseEvent.initEvent( 'mouseover', true, true );
      altTriggerDom.dispatchEvent( mouseEvent );
      altTriggerDom.click();
    } );
  } );

  describe( '.expand()', () => {
    beforeEach( () => {
      // Set up expected event listeners.
      expandBeginSpy = jest.fn();
      expandEndSpy = jest.fn();

      flyoutMenu.init();
      flyoutMenu.addEventListener( 'expandBegin', expandBeginSpy );
      flyoutMenu.addEventListener( 'expandEnd', expandEndSpy );
    } );

    afterEach( () => {
      // Check expected event broadcasts.
      expect( expandBeginSpy ).toHaveBeenCalledTimes( 1 );
      expect( expandBeginSpy ).toHaveBeenCalledWith(
        { target: flyoutMenu, type: 'expandBegin' }
      );

      expect( expandEndSpy ).toHaveBeenCalledTimes( 1 );
      expect( expandEndSpy ).toHaveBeenCalledWith(
        { target: flyoutMenu, type: 'expandEnd' }
      );

      // Check expected aria attributes state.
      expect( triggerDom.getAttribute( 'aria-expanded' ) ).toBe( 'true' );
      expect( contentDom.getAttribute( 'aria-expanded' ) ).toBe( 'true' );
      expect( altTriggerDom.getAttribute( 'aria-expanded' ) ).toBe( 'true' );
    } );

    it( 'should dispatch events and set aria attributes, ' +
        'when called by trigger click', () => {
      triggerDom.click();
    } );

    it( 'should dispatch events and set aria attributes, ' +
        'when called by alt trigger click', () => {
      altTriggerDom.click();
    } );

    it( 'should dispatch events and set aria attributes, ' +
        'when called directly', () => {
      flyoutMenu.expand();
    } );
  } );

  describe( '.collapse()', () => {
    beforeEach( () => {
      // Set up expected event listeners.
      collapseBeginSpy = jest.fn();
      collapseEndSpy = jest.fn();

      flyoutMenu.init();
      flyoutMenu.addEventListener( 'collapseBegin', collapseBeginSpy );
      flyoutMenu.addEventListener( 'collapseEnd', collapseEndSpy );
      triggerDom.click();
    } );

    afterEach( () => {
      // Check expected event broadcasts.
      expect( collapseBeginSpy ).toHaveBeenCalledTimes( 1 );
      expect( collapseBeginSpy ).toHaveBeenCalledWith(
        { target: flyoutMenu, type: 'collapseBegin' }
      );

      expect( collapseEndSpy ).toHaveBeenCalledTimes( 1 );
      expect( collapseEndSpy ).toHaveBeenCalledWith(
        { target: flyoutMenu, type: 'collapseEnd' }
      );

      // Check expected aria attribute states.
      expect( triggerDom.getAttribute( 'aria-expanded' ) ).toBe( 'false' );
      expect( contentDom.getAttribute( 'aria-expanded' ) ).toBe( 'false' );
      expect( altTriggerDom.getAttribute( 'aria-expanded' ) ).toBe( 'false' );
    } );

    it( 'should dispatch events and set aria attributes, ' +
        'when called by trigger click', () => {
      triggerDom.click();
    } );

    it( 'should dispatch events and set aria attributes, ' +
        'when called by alt trigger click', () => {
      altTriggerDom.click();
    } );

    it( 'should dispatch events and set aria attributes, ' +
        'when called directly', () => {
      flyoutMenu.collapse();
    } );
  } );

  describe( '.setExpandTransition()', () => {
    it( 'should set a transition', done => {
      flyoutMenu.init();
      const transition = new MoveTransition( contentDom ).init();
      flyoutMenu.setExpandTransition( transition, transition.moveLeft );
      flyoutMenu.addEventListener( 'expandEnd', () => {
        try {
          const hasClass = contentDom.classList.contains( 'u-move-transition' );
          expect( hasClass ).toBe( true );
          done();
        } catch ( err ) {
          done( err );
        }
      } );
      triggerDom.click();

      /* The transitionend event should fire on its own,
         but for some reason the transitionend event is not firing within JSDom.
         In a future JSDom update this should be revisited.
         See https://github.com/jsdom/jsdom/issues/1781
      */
      const event = new Event( 'transitionend' );
      event.propertyName = 'transform';
      contentDom.dispatchEvent( event );
    } );
  } );

  describe( '.setCollapseTransition()', () => {
    it( 'should set a transition', done => {
      flyoutMenu.init();
      const transition = new MoveTransition( contentDom ).init();
      triggerDom.click();
      flyoutMenu.setCollapseTransition( transition, transition.moveLeft );
      flyoutMenu.addEventListener( 'collapseEnd', () => {
        try {
          const hasClass = contentDom.classList.contains( 'u-move-transition' );
          expect( hasClass ).toBe( true );
          done();
        } catch ( err ) {
          done( err );
        }
      } );
      triggerDom.click();

      /* The transitionend event should fire on its own,
         but for some reason the transitionend event is not firing within JSDom.
         In a future JSDom update this should be revisited.
         See https://github.com/jsdom/jsdom/issues/1781
      */
      const event = new Event( 'transitionend' );
      event.propertyName = 'transform';
      contentDom.dispatchEvent( event );
    } );
  } );

  describe( '.getTransition()', () => {
    it( 'should return a transition instance', () => {
      flyoutMenu.init();
      expect( flyoutMenu.getTransition() ).toBeUndefined();
      const transition = new MoveTransition( contentDom ).init();
      flyoutMenu.setExpandTransition( transition, transition.moveLeft );
      flyoutMenu.setCollapseTransition( transition, transition.moveToOrigin );
      expect( flyoutMenu.getTransition() ).toStrictEqual( transition );
      expect( flyoutMenu.getTransition( FlyoutMenu.COLLAPSE_TYPE ) )
        .toStrictEqual( transition );
    } );
  } );

  describe( '.clearTransitions()', () => {
    it( 'should remove all transitions', () => {
      flyoutMenu.init();
      const transition = new MoveTransition( contentDom ).init();
      flyoutMenu.setExpandTransition( transition, transition.moveLeft );
      flyoutMenu.setCollapseTransition( transition, transition.moveToOrigin );
      let hasClass = contentDom.classList.contains( 'u-move-transition' );
      expect( hasClass ).toBe( true );
      flyoutMenu.clearTransitions();
      expect( flyoutMenu.getTransition() ).toBeUndefined();
      hasClass = contentDom.classList.contains( 'u-move-transition' );
      expect( hasClass ).toBe( false );
    } );
  } );

  describe( '.getDom()', () => {
    it( 'should return references to full dom', () => {
      flyoutMenu.init();
      const dom = flyoutMenu.getDom();
      expect( dom.container ).toStrictEqual( containerDom );
      expect( dom.trigger[0] ).toStrictEqual( triggerDom );
      expect( dom.content ).toStrictEqual( contentDom );
      expect( dom.trigger[1] ).toStrictEqual( altTriggerDom );
    } );
  } );

  describe( 'suspend/resume behavior', () => {
    beforeEach( () => {
      // Set up expected event listeners.
      expandBeginSpy = jest.fn();
      expandEndSpy = jest.fn();
      collapseBeginSpy = jest.fn();
      collapseEndSpy = jest.fn();
      flyoutMenu.init();
      flyoutMenu.addEventListener( 'expandBegin', expandBeginSpy );
      flyoutMenu.addEventListener( 'expandEnd', expandEndSpy );
      flyoutMenu.addEventListener( 'collapseBegin', collapseBeginSpy );
      flyoutMenu.addEventListener( 'collapseEnd', collapseEndSpy );
    } );

    describe( '.suspend()', () => {
      it( 'should not broadcast events after being suspended', () => {
        // Set up expected event listeners.
        flyoutMenu.suspend();
        triggerDom.click();

        expect( expandBeginSpy ).toHaveBeenCalledTimes( 0 );
        expect( expandEndSpy ).toHaveBeenCalledTimes( 0 );
        expect( collapseBeginSpy ).toHaveBeenCalledTimes( 0 );
        expect( collapseEndSpy ).toHaveBeenCalledTimes( 0 );
      } );
    } );

    describe( '.resume()', () => {
      it( 'should broadcast events after resuming from suspended', () => {
        // Set up expected event listeners.
        flyoutMenu.suspend();
        flyoutMenu.resume();
        triggerDom.click();

        expect( expandBeginSpy ).toHaveBeenCalledTimes( 1 );
        expect( expandEndSpy ).toHaveBeenCalledTimes( 1 );
        triggerDom.click();
        expect( collapseBeginSpy ).toHaveBeenCalledTimes( 1 );
        expect( collapseEndSpy ).toHaveBeenCalledTimes( 1 );
      } );
    } );

  } );

  describe( '.setData()', () => {
    it( 'should return the instance when set', () => {
      flyoutMenu.init();
      const inst = flyoutMenu.setData( 'test-data' );
      expect( inst ).toBeInstanceOf( FlyoutMenu );
    } );
  } );

  describe( '.getData()', () => {
    it( 'should return the set data', () => {
      flyoutMenu.init();
      flyoutMenu.setData( 'test-data' );
      expect( flyoutMenu.getData() ).toBe( 'test-data' );
    } );
  } );

  describe( '.isAnimating()', () => {
    it( 'should return true when expanding', done => {
      flyoutMenu.init();
      flyoutMenu.addEventListener( 'expandBegin', () => {
        try {
          expect( flyoutMenu.isAnimating() ).toBe( true );
          done();
        } catch ( err ) {
          done( err );
        }
      } );
      triggerDom.click();
    } );

    it( 'should return false after expanding', done => {
      flyoutMenu.init();
      flyoutMenu.addEventListener( 'expandEnd', () => {
        try {
          expect( flyoutMenu.isAnimating() ).toBe( false );
          done();
        } catch ( err ) {
          done( err );
        }
      } );
      triggerDom.click();
    } );

    it( 'should return true while collapsing', done => {
      flyoutMenu.init();
      flyoutMenu.addEventListener( 'collapseBegin', () => {
        try {
          expect( flyoutMenu.isAnimating() ).toBe( true );
          done();
        } catch ( err ) {
          done( err );
        }
      } );
      triggerDom.click();
      triggerDom.click();
    } );

    it( 'should return false after collapsing', done => {
      flyoutMenu.init();
      flyoutMenu.addEventListener( 'collapseEnd', () => {
        try {
          expect( flyoutMenu.isAnimating() ).toBe( false );
          done();
        } catch ( err ) {
          done( err );
        }
      } );
      triggerDom.click();
      triggerDom.click();
    } );
  } );

  describe( '.isExpanded()', () => {
    it( 'should return false before expanding', done => {
      flyoutMenu.init();
      flyoutMenu.addEventListener( 'expandBegin', () => {
        try {
          expect( flyoutMenu.isExpanded() ).toBe( false );
          done();
        } catch ( err ) {
          done( err );
        }
      } );
      triggerDom.click();
    } );

    it( 'should return true after expanding', done => {
      flyoutMenu.init();
      flyoutMenu.addEventListener( 'expandEnd', () => {
        try {
          expect( flyoutMenu.isExpanded() ).toBe( true );
          done();
        } catch ( err ) {
          done( err );
        }
      } );
      triggerDom.click();
    } );

    it( 'should return true before collapsing', done => {
      flyoutMenu.init();
      triggerDom.click();
      flyoutMenu.addEventListener( 'triggerClick', () => {
        try {
          expect( flyoutMenu.isExpanded() ).toBe( true );
          done();
        } catch ( err ) {
          done( err );
        }
      } );
      triggerDom.click();
    } );

    it( 'should return false after collapsing', done => {
      flyoutMenu.init();
      flyoutMenu.addEventListener( 'collapseEnd', () => {
        try {
          expect( flyoutMenu.isExpanded() ).toBe( false );
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
