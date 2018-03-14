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

function scrollTo( xCoord, yCoord ) {
  window.scrollX = xCoord;
  window.scrollY = yCoord;
}

function requestAnimationFrame( callback ) {
  const currTime = new Date().getTime();
  const timeToCall = Math.max( 0, 16 - ( currTime - lastTime ) );
  const id = window.setTimeout(
    function() {
      callback( currTime + timeToCall );
    }, timeToCall
  );

  lastTime = currTime + timeToCall;

  return id;
}

describe( 'Footer', () => {
  beforeAll( () => {
    document.body.innerHTML = HTML_SNIPPET;

    global.NodeList = window.NodeList;
    global.Node = window.Node;
  } );

  beforeEach( () => {
    bodyDom = document.body;
    bodyDom.innerHTML = HTML_SNIPPET;
    footerBtnDom = document.querySelector( '.o-footer_top-button' );

    window.requestAnimationFrame = requestAnimationFrame;
    window.scrollTo = scrollTo;
  } );

  it( 'button should initiate scroll to page top when clicked', done => {
    window.scrollY = 10;
    FooterButton.init();
    triggerClick( footerBtnDom );
    // this.timeout( 3000 );
    window.setTimeout( () => {
      expect( window.scrollY ).toEqual( 0 );
      done();
    }, 2000 );
  } );
} );
