const BASE_JS_PATH = '../../../../../cfgov/unprocessed/apps/';
const hud = require( BASE_JS_PATH + 'find-a-housing-counselor/js/hud-util' );

describe( 'hud', () => {

  describe( 'checkHudData', () => {
    it( 'Should return true on a valid HUD data, false otherwise.', () => {
      const mockData = {
        // eslint-disable-next-line camelcase
        counseling_agencies: [ { } ],
        zip: { }
      };
      expect( hud.checkHudData( mockData ) ).toBe( true );
      expect( hud.checkHudData( '' ) ).toBe( false );
      expect( hud.checkHudData( null ) ).toBe( false );
    } );
  } );

} );
