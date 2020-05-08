const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';
const FooterButton = require( BASE_JS_PATH + 'modules/footer-button.js' );

import { simulateEvent } from '../../../util/simulate-event';

let footerBtnDom;

const HTML_SNIPPET = `
<div class="skip-nav">
    <a class="skip-nav_link" href="#main">
        Skip to main content
    </a>
</div>
<a class="a-btn a-btn__secondary o-footer_top-button"
   data-gtm_ignore="true" data-js-hook="behavior_return-to-top"
   href="#">
    Back to top
</a>
`;

/**
 * Mock window.scrollTo() method.
 * @param  {number} xCoord An x coordinate.
 * @param  {number} yCoord A y coordinate.
 */
function scrollTo( xCoord, yCoord ) {
  window.scrollX = xCoord;
  window.scrollY = yCoord;
}

describe( 'footer-button', () => {
  beforeAll( () => {
    window.scrollTo = scrollTo;
    document.body.innerHTML = HTML_SNIPPET;
    footerBtnDom = document.querySelector( '.o-footer_top-button' );
  } );

  it( 'button should scroll when clicked ' +
      'and requestAnimationFrame is supported', done => {
    window.scrollY = 10;
    FooterButton.init();
    simulateEvent( 'click', footerBtnDom );

    window.setTimeout( () => {
      expect( window.scrollY ).toBe( 0 );
      done();
    }, 2000 );
  } );

  it( 'button should scroll when clicked ' +
      'and requestAnimationFrame is not supported', () => {
    jest.spyOn( window, 'scrollTo' );
    delete window.requestAnimationFrame;
    window.scrollY = 10;
    FooterButton.init();
    simulateEvent( 'click', footerBtnDom );

    expect( window.scrollTo ).toHaveBeenCalledWith( 0, 0 );
  } );
} );
