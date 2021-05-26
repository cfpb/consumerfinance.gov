import HTML_SNIPPET from '../../mocks/megaMenuSnippet.js';
import MegaMenu from '../../../../cfgov/unprocessed/js/organisms/MegaMenu.js';
import { simulateEvent } from '../../../util/simulate-event.js';

describe( 'MegaMenu', () => {
  let navElem;
  let megaMenu;

  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
    navElem = document.querySelector( '.o-mega-menu' );
    megaMenu = new MegaMenu( navElem );
    megaMenu.init();
  } );

  describe( 'sub-menu click handler', () => {

    /* CAUTION: With the addition of manually firing the transitionend event
       for some reason this test fails if it's not the first test.
       Revisit changing the order of this test when JSDom supports transition
       events fully.
       See https://github.com/jsdom/jsdom/issues/1781
    */
    it( 'should expand on the first level sub-menu button click', done => {
      window.innerWidth = 420;
      const menuTrigger = navElem.querySelector( '.o-mega-menu_trigger' );
      const subTrigger = navElem.querySelector( '.o-mega-menu_content-1-link__has-children' );
      const subContent = navElem.querySelector( '.o-mega-menu_content-2' );
      const subContentWrapper = navElem.querySelector( '.o-mega-menu_content-2-wrapper' );
      let isExpanded;

      function resolveFirstClick() {
        simulateEvent( 'click', subTrigger );

        /* The transitionend event should fire on its own,
           but for some reason the transitionend event is not firing within JSDom.
           In a future JSDom update this should be revisited.
           See https://github.com/jsdom/jsdom/issues/1781
        */
        const event = new Event( 'transitionend' );
        event.propertyName = 'transform';
        subContentWrapper.dispatchEvent( event );

        window.setTimeout( resolveSecondClick, 1000 );
      }

      function resolveSecondClick() {
        isExpanded = subContent.getAttribute( 'aria-expanded' );

        expect( isExpanded ).toEqual( 'true' );
        done();
      }

      simulateEvent( 'click', menuTrigger );

      window.setTimeout( resolveFirstClick, 1000 );
    } );

    it( 'should not be expanded by default', () => {
      window.innerWidth = 420;
      const subContent = navElem.querySelector( '.o-mega-menu_content-2' );
      const isExpanded = subContent.getAttribute( 'aria-expanded' );

      expect( isExpanded ).toEqual( 'false' );
    } );

    it( 'should not be expanded on the main trigger click', done => {
      window.innerWidth = 420;
      const menuTrigger = navElem.querySelector( '.o-mega-menu_trigger' );
      const subContent = navElem.querySelector( '.o-mega-menu_content-2' );
      let isExpanded;

      function resolveFirstClick() {
        isExpanded = subContent.getAttribute( 'aria-expanded' );

        expect( isExpanded ).toEqual( 'false' );
        done();
      }

      simulateEvent( 'click', menuTrigger );

      window.setTimeout( resolveFirstClick, 1000 );
    } );

    it( 'should collapse on the first level sub-menu back button click', done => {
      window.innerWidth = 420;
      const menuTrigger = navElem.querySelector( '.o-mega-menu_trigger' );
      const subTrigger = navElem.querySelector( '.o-mega-menu_content-1-link__has-children' );
      const subContent = navElem.querySelector( '.o-mega-menu_content-2' );
      const subAltTrigger = subContent.querySelector( '.o-mega-menu_content-alt-trigger' );
      let isExpanded;

      function resolveFirstClick() {
        simulateEvent( 'click', subTrigger );

        window.setTimeout( resolveSecondClick, 1000 );
      }

      function resolveSecondClick() {
        simulateEvent( 'click', subAltTrigger );

        window.setTimeout( resolveThirdClick, 1000 );
      }

      function resolveThirdClick() {
        isExpanded = subContent.getAttribute( 'aria-expanded' );

        expect( isExpanded ).toEqual( 'false' );
        done();
      }

      simulateEvent( 'click', menuTrigger );

      window.setTimeout( resolveFirstClick, 1000 );
    } );
  } );
} );
