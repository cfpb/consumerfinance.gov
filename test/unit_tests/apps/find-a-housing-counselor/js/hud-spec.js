const BASE_JS_PATH = '../../../../../cfgov/unprocessed/apps/';
const hud = require( BASE_JS_PATH + 'find-a-housing-counselor/js/hud.js' );

let UNDEFINED;

describe( 'hud', () => {

  describe( 'checkZip', () => {
    it( 'Should return true on a valid zipcode, false otherwise.', () => {
      expect( hud.checkZip( '05201' ) ).toBe( true );
      expect( hud.checkZip( '' ) ).toBe( false );
      expect( hud.checkZip( null ) ).toBe( false );
      expect( hud.checkZip( UNDEFINED ) ).toBe( false );
      expect( hud.checkZip( false ) ).toBe( false );
    } );
  } );

  describe( 'checkHudData', () => {
    it( 'Should return true on a valid HUD data, false otherwise.', () => {
      const mockData = {
        counseling_agencies: [ { } ],
        zip: { }
      };
      expect( hud.checkHudData( mockData ) ).toBe( true );
      expect( hud.checkHudData( '' ) ).toBe( false );
      expect( hud.checkHudData( null ) ).toBe( false );
    } );
  } );

  describe( 'getURLQueryVariable', () => {

    beforeEach( () => history.replaceState( {}, 'Home', '/?zipcode=05201' ) );

    it( 'Should return true on a valid HUD data, false otherwise.', () => {
      expect( hud.getURLQueryVariable( 'zipcode' ) ).toBe( '05201' );
      expect( hud.getURLQueryVariable( 'nothing' ) ).toBe( '' );
    } );
  } );

} );
