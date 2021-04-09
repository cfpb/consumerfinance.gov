const BASE_JS_PATH = '../../../../../cfgov/unprocessed/apps/';
const scroll = require(
  BASE_JS_PATH + 'teachers-digital-platform/js/scroll.js'
);

const HTML_SNIPPET = `
  <a class="one" href="#one" data-scroll>one</a>
  <a class="two" href="#two" data-scroll>two</a>
  <a class="three" href="#three" data-scroll>three</a>
  <div id="one"></div>
  <div id="two"></div>
  <div id="three"></div>
`;

// Helper function to simulate events
function simulateEvent( eventType, target, eventOption ) {
  const event = document.createEvent( 'Event' );
  if ( eventOption && eventOption.keyCode ) {
    event.keyCode = eventOption.keyCode;
  }
  event.initEvent( eventType, true, true );
  return target.dispatchEvent( event );
}

/* eslint-disable max-lines-per-function, no-undefined */
describe( 'Scroll', () => {

  beforeEach( () => {
    // Load HTML fixture
    document.body.innerHTML = HTML_SNIPPET;
    global.scroll = jest.fn();
    scroll.init();
  } );

  afterEach( () => {
    document.body.innerHTML = '';
  } );

  it( 'should update the URL when clicked', () => {
    const spy = jest.spyOn( global.history, 'pushState' );

    scroll.init();
    const jumplink = document.querySelector( '.one' );

    simulateEvent( 'click', jumplink );

    expect( spy ).toHaveBeenCalledWith( null, null, '#one' );
  } );

} );
