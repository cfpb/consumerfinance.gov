import SummaryMobile from '../../../../cfgov/unprocessed/js/organisms/SummaryMobile.js';
import { simulateEvent } from '../../../util/simulate-event';

const HTML_SNIPPET = `
<div class="o-summary-mobile"
     data-js-hook="behavior_flyout-menu">
    <div class="o-summary-mobile_content"
         data-js-hook="behavior_flyout-menu_content">
        Content
    </div>
    <button class="o-summary-mobile_btn"
            data-js-hook="behavior_flyout-menu_trigger">
        Read full description
    </button>
</div>
`;

let summaryMobile;
let summaryMobileDom;
let targetDom;
let contentDom;

/**
 * Change the viewport to width x height. Mocks window.resizeTo( w, h ).
 * @param  {number} width - width in pixels.
 * @param  {number} height - height in pixels.
 */
function windowResizeTo( width, height ) {
  // Change the viewport to width x height. Mocks window.resizeTo( w, h ).
  global.innerWidth = width;
  global.innerHeight = height;

  // Trigger the window resize event.
  global.dispatchEvent( new Event( 'resize' ) );
}

describe( 'Summary Mobile', () => {

  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
    summaryMobileDom = document.querySelector( '.o-summary-mobile' );
    targetDom = summaryMobileDom.querySelector( '.o-summary-mobile_btn' );
    contentDom = summaryMobileDom.querySelector( '.o-summary-mobile_content' );

    summaryMobile = new SummaryMobile( summaryMobileDom );
  } );

  describe( 'initialized state', () => {
    it( 'should be initialized', () => {
      expect( summaryMobileDom.getAttribute( 'data-js-hook' ) ).toBe( 'behavior_flyout-menu' );
      summaryMobile.init();
      expect( summaryMobileDom.getAttribute( 'data-js-hook' ) ).toBe( 'behavior_flyout-menu state_atomic_init' );
    } );
  } );

  describe( 'interactions', () => {
    it( 'should expand on click', () => {
      summaryMobile.init();
      windowResizeTo( 300 );
      expect( contentDom.getAttribute( 'aria-expanded' ) ).toBe( 'false' );
      expect( targetDom.getAttribute( 'aria-expanded' ) ).toBe( 'false' );
      simulateEvent( 'click', targetDom );

      /* The transitionend event should fire on its own,
         but for some reason the transitionend event is not firing within JSDom.
         In a future JSDom update this should be revisited.
         See https://github.com/jsdom/jsdom/issues/1781
      */
      const event = new Event( 'transitionend' );
      event.propertyName = 'max-height';
      contentDom.dispatchEvent( event );

      expect( contentDom.style.maxHeight ).not.toBe( '0' );
      expect( contentDom.getAttribute( 'aria-expanded' ) ).toBe( 'true' );
      expect( targetDom.getAttribute( 'aria-expanded' ) ).toBe( 'true' );

      expect( targetDom.classList.contains( 'u-hidden' ) ).toBe( true );
      windowResizeTo( 1200 );
    } );
  } );
} );
