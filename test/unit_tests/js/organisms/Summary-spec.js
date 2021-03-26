import Summary from '../../../../cfgov/unprocessed/js/organisms/Summary.js';
import { simulateEvent } from '../../../util/simulate-event';

const HTML_SNIPPET = `
<div class="o-summary o-summary__mobile"
     data-js-hook="behavior_flyout-menu">
    <div class="o-summary_content"
         data-js-hook="behavior_flyout-menu_content">
        Content
    </div>
    <button class="o-summary_btn u-hidden"
            data-js-hook="behavior_flyout-menu_trigger">
        Read full description
    </button>
</div>
`;

let summary;
let summaryDom;
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

describe( 'Summary', () => {

  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
    summaryDom = document.querySelector( '.o-summary__mobile' );
    targetDom = summaryDom.querySelector( '.o-summary_btn' );
    contentDom = summaryDom.querySelector( '.o-summary_content' );

    summary = new Summary( summaryDom );
  } );

  describe( 'initialized state', () => {
    it( 'should be initialized', () => {
      expect( summaryDom.getAttribute( 'data-js-hook' ) ).toBe( 'behavior_flyout-menu' );
      summary.init();
      expect( summaryDom.getAttribute( 'data-js-hook' ) ).toBe( 'behavior_flyout-menu state_atomic_init' );
    } );
  } );

  describe( 'interactions', () => {

    it( 'should be absent when content is too brief', () => {
      jest.spyOn( contentDom, 'offsetHeight', 'get' )
        .mockImplementation( () => 50 );
      summary.init();
      windowResizeTo( 300 );
      expect( contentDom.getAttribute( 'aria-expanded' ) ).toBe( null );
      expect( targetDom.classList.contains( 'u-hidden' ) ).toBe( true );
    } );

    it( 'should expand on click', () => {
      jest.spyOn( contentDom, 'offsetHeight', 'get' )
        .mockImplementation( () => 200 );
      summary.init();
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
