const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';
const FooterButton = require( BASE_JS_PATH + 'modules/footer-button.js' );

import { simulateEvent } from '../../../util/simulate-event';

let footerBtnDom;

const HTML_SNIPPET = `
  <a class="a-btn a-btn__secondary o-footer_top-button"
     data-gtm_ignore="true" data-js-hook="behavior_return-to-top"
     href="#">
      Back to top <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 699.6 1200" class="cf-icon-svg"><path d="M681 464.8L395.8 179.6c-25.4-25.4-66.5-25.4-91.9 0L18.6 464.8c-25.1 25.6-24.8 66.8.8 91.9 25.3 24.8 65.8 24.8 91.1 0l174.3-174.3v601.8c0 35.9 29.1 65 65 65s65-29.1 65-65V382.4l174.3 174.3c25.6 25.1 66.8 24.8 91.9-.8 24.8-25.3 24.8-65.8 0-91.1z"/></svg>
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
  } );

  beforeEach( () => {
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
