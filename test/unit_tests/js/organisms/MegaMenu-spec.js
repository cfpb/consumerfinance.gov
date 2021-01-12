import MegaMenu from '../../../../cfgov/unprocessed/js/organisms/MegaMenu';
import { simulateEvent } from '../../../util/simulate-event';
import HTML_SNIPPET from '../../mocks/megaMenuSnippet';

describe( 'MegaMenu', () => {
  let navElem;
  let megaMenu;
  let thisMegaMenu;

  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
    navElem = document.querySelector( '.o-mega-menu' );
    megaMenu = new MegaMenu( navElem );
    thisMegaMenu = megaMenu.init();
  } );

  describe( 'init()', () => {
    it( 'should return the MegaMenu instance when initialized', () => {
      expect( typeof thisMegaMenu ).toStrictEqual( 'object' );
      expect( navElem.dataset.jsHook ).toContain( 'state_atomic_init' );
    } );

    it( 'should return undefined if already initialized', () => {
      expect( megaMenu.init() ).toBeUndefined();
    } );
  } );

  describe( 'collapse', () => {
    it( 'should not be expanded by default', () => {
      window.innerWidth = 420;
      const firstContent = navElem.querySelector( '.o-mega-menu_content-1' );
      const defaultExpanded = firstContent.getAttribute( 'aria-expanded' );

      expect( defaultExpanded ).toEqual( 'false' );
    } );

    it( 'should expand on click', done => {
      window.innerWidth = 420;
      const firstContent = navElem.querySelector( '.o-mega-menu_content-1' );
      const menuTrigger = navElem.querySelector( '.o-mega-menu_trigger' );
      let isExpanded;

      function resolveClick() {
        isExpanded = firstContent.getAttribute( 'aria-expanded' );
        expect( isExpanded ).toEqual( 'true' );
        done();
      }

      simulateEvent( 'click', menuTrigger );

      /* The transitionend event should fire on its own,
         but for some reason the transitionend event is not firing within JSDom.
         In a future JSDom update this should be revisited.
         See https://github.com/jsdom/jsdom/issues/1781
      */
      const event = new Event( 'transitionend' );
      event.propertyName = 'transform';
      firstContent.dispatchEvent( event );

      window.setTimeout( resolveClick, 1000 );
    } );

    it( 'should close when calling the collapse method', done => {
      window.innerWidth = 420;
      const firstContent = navElem.querySelector( '.o-mega-menu_content-1' );
      const menuTrigger = navElem.querySelector( '.o-mega-menu_trigger' );
      let isExpanded;

      function resolveClick() {
        megaMenu.collapse();
        isExpanded = firstContent.getAttribute( 'aria-expanded' );
        expect( isExpanded ).toEqual( 'false' );
        done();
      }

      simulateEvent( 'click', menuTrigger );

      window.setTimeout( resolveClick, 1000 );
    } );
  } );
} );
