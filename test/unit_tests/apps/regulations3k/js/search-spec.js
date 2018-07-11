const simulateEvent = require( '../../../../util/simulate-event' ).simulateEvent;
const BASE_JS_PATH = '../../../../../cfgov/unprocessed/apps/regulations3k';

const app = require( `${ BASE_JS_PATH }/js/search.js` );

const HTML_SNIPPET = `
  <input id="query" name="q" type="text" title="Search terms" class="a-text-input" value="money" placeholder="Search terms">
  <div>
    <div class="m-form-field m-form-field__checkbox reg-checkbox">
      <input class="a-checkbox" type="checkbox" value="1002" id="regulation-1002" name="regs">
      <label class="a-label" for="regulation-1002">
          1002 (Regulation B)
      </label>
    </div>
  </div>
  <div>
    <button class="a-tag" type="button" value="1002" data-js-hook="behavior_clear-filter">
    1002 (Regulation B)
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 718.9 1200" class="cf-icon-svg">
      </svg>
    </button>
  </div>
  <button id="clear-all" data-js-hook="behavior_clear-all">
      Clear all filters
  </button>
  <div id="regs3k-results"></div>
`;

const xhr = global.XMLHttpRequest;
global.console = { error: jest.fn(), log: jest.fn() };

describe( 'The Regs3K search page', () => {

  beforeEach( () => {
    // Reset global XHR
    global.XMLHttpRequest = xhr;
    // Load HTML fixture
    document.body.innerHTML = HTML_SNIPPET;
    // Fire `load` event
    const event = document.createEvent( 'Event' );
    event.initEvent( 'load', true, true );
    window.dispatchEvent( event );
  } );

  it( 'should not throw any errors on init', () => {
    expect( () => app ).not.toThrow();
  } );

  it( 'should clear a filter when its X icon is clicked', () => {
    const mockXHR = {
      open: jest.fn(),
      send: jest.fn(),
      readyState: 4,
      status: 200,
      onreadystatechange: jest.fn(),
      responseText: []
    };
    global.XMLHttpRequest = jest.fn( () => mockXHR );
    const clearIcon = document.querySelector( 'svg' );

    let numFilters = document.querySelectorAll( 'button.a-tag' ).length;
    expect( numFilters ).toEqual( 1 );

    simulateEvent( 'click', clearIcon );
    numFilters = document.querySelectorAll( 'button.a-tag' ).length;
    expect( numFilters ).toEqual( 0 );

    mockXHR.onreadystatechange();
  } );

  it( 'should not clear a filter when its tag is clicked', () => {
    const button = document.querySelector( 'button.a-tag' );

    let numFilters = document.querySelectorAll( 'button.a-tag' ).length;
    expect( numFilters ).toEqual( 1 );

    simulateEvent( 'click', button );
    numFilters = document.querySelectorAll( 'button.a-tag' ).length;
    expect( numFilters ).toEqual( 1 );
  } );

  it( 'should clear all filters the `clear all` link is clicked', () => {
    const mockXHR = {
      open: jest.fn(),
      send: jest.fn(),
      readyState: 4,
      status: 200,
      onreadystatechange: jest.fn(),
      responseText: []
    };
    global.XMLHttpRequest = jest.fn( () => mockXHR );
    const clearAllLink = document.querySelector( '#clear-all' );

    let numFilters = document.querySelectorAll( 'button.a-tag' ).length;
    expect( numFilters ).toEqual( 1 );

    simulateEvent( 'click', clearAllLink );
    numFilters = document.querySelectorAll( 'button.a-tag' ).length;
    expect( console.log ).toBeCalled();

    mockXHR.onreadystatechange();
  } );

  it( 'should handle errors when the server is down', done => {
    const mockXHR = {
      open: jest.fn(),
      send: jest.fn(),
      readyState: 4,
      status: 404,
      onreadystatechange: jest.fn(),
      responseText: 'Server error!'
    };
    global.XMLHttpRequest = jest.fn( () => mockXHR );
    const clearIcon = document.querySelector( 'svg' );

    simulateEvent( 'click', clearIcon );
    setTimeout( () => {
      expect( console.error ).toBeCalled();
      done();
    }, 100 );

    mockXHR.onreadystatechange();
  } );

} );
