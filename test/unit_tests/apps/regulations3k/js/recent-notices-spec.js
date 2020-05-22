import { simulateEvent } from '../../../../util/simulate-event';
const BASE_JS_PATH = '../../../../../cfgov/unprocessed/apps/regulations3k';

const HTML_SNIPPET = `
  <ul id="regs3k-notices"></ul>
`;

const TEST_DATA = {
  results: [
    {
      html_url: 'https://example.com',
      title: 'Notice A'
    },
    {
      html_url: 'https://example.com',
      title: 'Notice B'
    },
    {
      html_url: 'https://example.com',
      title: 'Notice C'
    }
  ]
};

// Back up global xhr
const xhr = global.XMLHttpRequest;

// Mock console logging
delete global.console;
global.console = { error: jest.fn(), log: jest.fn() };

// Reference to the script recent-notices.js
let app;

describe( 'The Regs3K search page', () => {

  beforeEach( () => {
    app = require( `${ BASE_JS_PATH }/js/recent-notices.js` );

    // Load HTML fixture
    document.body.innerHTML = HTML_SNIPPET;
  } );

  afterEach( () => {
    // Reset global XHR
    global.XMLHttpRequest = xhr;
  } );

  it( 'should process a notice', () => {
    const notice = {
      html_url: 'https://federalregister.gov/',
      title: 'Really great notice'
    };
    const processedNotice = app.processNotice( notice );
    expect( processedNotice.constructor.name ).toEqual( 'HTMLLIElement' );
    expect( processedNotice.className ).toEqual( 'm-list_link' );
    expect( processedNotice.querySelector( 'a' ).href ).toEqual( 'https://federalregister.gov/' );
  } );

  it( 'should process notices', () => {
    const notices = [
      {
        html_url: 'https://federalregister.gov/1',
        title: 'Really great notice'
      },
      {
        html_url: 'https://federalregister.gov/2',
        title: 'Another really great notice'
      }
    ];
    const processedNotices = app.processNotices( notices );
    expect( processedNotices.querySelectorAll( 'li' ).length ).toEqual( 3 );
    expect( processedNotices.querySelectorAll( 'a' )[2].textContent ).toContain( 'More' );
  } );

  it( 'should load recent notices', () => {
    // Mock the browser's XHR
    const mockXHR = {
      open: jest.fn(),
      send: jest.fn(),
      readyState: 4,
      status: 200,
      responseText: JSON.stringify( TEST_DATA )
    };
    global.XMLHttpRequest = jest.fn( () => mockXHR );

    // Fire `load` event
    simulateEvent( 'load', window, { currentTarget: window } );

    // Complete XHR
    mockXHR.onreadystatechange();

    const numNotices = document.querySelectorAll( '.m-list_link' ).length;
    expect( numNotices ).toEqual( 4 );
  } );

  it( 'should fail to load recent notices', done => {
    // Mock the browser's XHR
    const mockXHR = {
      open: jest.fn(),
      send: jest.fn(),
      readyState: 4,
      status: 404,
      onreadystatechange: jest.fn(),
      responseText: 'Server error!'
    };
    global.XMLHttpRequest = jest.fn( () => mockXHR );

    // Fire `load` event
    simulateEvent( 'load', window, { currentTarget: window } );

    // Complete XHR
    mockXHR.onreadystatechange();

    setTimeout( () => {
      expect( console.error ).toBeCalled();
      done();
    }, 100 );
  } );

} );
