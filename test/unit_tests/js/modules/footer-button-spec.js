const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';
const FooterButton = require( BASE_JS_PATH + 'modules/footer-button.js' );

let footerBtnDom;
let bodyDom;
let lastTime = 0;

const HTML_SNIPPET = `
  <a class="a-btn a-btn__secondary o-footer_top-button"
     data-gtm_ignore="true" data-js-hook="behavior_return-to-top"
     href="#">
      Back to top <span class="cf-icon cf-icon-arrow-up"></span>
  </a>
`;

function scrollTo( xCoord, yCoord ) {
  window.scrollX = xCoord;
  window.scrollY = yCoord;
}

/**
 * Simulate a click event
 * @param  {HTMLNode} target - Element that dispatches the click event.
 */
function triggerClick( target ) {
  const clickEvent = new window.MouseEvent( 'click', {
    bubbles: true,
    cancelable: true,
    view: window
  } );

  target.dispatchEvent( clickEvent );
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
    triggerClick( footerBtnDom );

    window.setTimeout( () => {
      expect( window.scrollY ).toBe( 0 );
      done();
    }, 1000 );
  } );

  it( 'button should scroll when clicked ' +
      'and requestAnimationFrame is not supported', () => {
    spyOn( window, 'scrollTo' );
    delete window.requestAnimationFrame;
    window.scrollY = 10;
    FooterButton.init();
    triggerClick( footerBtnDom );

    expect( window.scrollTo ).toHaveBeenCalledWith( 0, 0 );
  } );
} );
