import '../../../../cfgov/unprocessed/js/admin/global';

describe( 'Environment banner', () => {
  it( 'should create data attribute on page load', () => {
    expect( document.body.getAttribute( 'data-env' ) ).not.toBe( null );
  } );
} );
