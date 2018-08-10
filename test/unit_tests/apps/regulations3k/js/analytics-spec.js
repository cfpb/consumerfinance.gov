const BASE_JS_PATH = '../../../../../cfgov/unprocessed/apps/regulations3k';

const analytics = require( `${ BASE_JS_PATH }/js/analytics.js` );

describe( 'The Regs3K analytics', () => {

  it( 'should send events', () => {
    const event = analytics.sendEvent( 'click', 'sidebar' );

    expect( event ).toEqual( {
      event: 'eRegs Event',
      action: 'click',
      label: 'sidebar',
      eventCallback: undefined,
      eventTimeout: 500
    } );
  } );

  it( 'should send events with custom categories', () => {
    const event = analytics.sendEvent( 'click', 'sidebar', 'eregs' );

    expect( event ).toEqual( {
      event: 'eregs',
      action: 'click',
      label: 'sidebar',
      eventCallback: undefined,
      eventTimeout: 500
    } );
  } );

} );
