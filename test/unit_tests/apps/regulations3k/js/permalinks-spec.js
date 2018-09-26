const BASE_JS_PATH = '../../../../../cfgov/unprocessed/apps/regulations3k';

const app = require( `${ BASE_JS_PATH }/js/permalinks.js` );

describe( 'Permalinks functionality', () => {

  beforeEach( () => {
    // Fire `load` event
    const event = document.createEvent( 'Event' );
    event.initEvent( 'load', true, true );
    window.dispatchEvent( event );
  } );

  it( 'should not throw any errors on init', () => {
    expect( () => app ).not.toThrow();
  } );

} );
