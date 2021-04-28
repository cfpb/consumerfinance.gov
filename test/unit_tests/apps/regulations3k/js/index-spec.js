import {
  app
} from '../../../../../cfgov/unprocessed/apps/regulations3k/js/index.js';

describe( 'The app', () => {

  it( 'should not throw any errors on init', () => {
    expect( () => app ).not.toThrow();
  } );

} );
