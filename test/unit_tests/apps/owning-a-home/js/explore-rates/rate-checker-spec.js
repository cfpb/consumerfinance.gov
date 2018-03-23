const BASE_JS_PATH = '../../../../../../cfgov/unprocessed/apps/owning-a-home/';
const rateChecker = require( BASE_JS_PATH + 'js/explore-rates/rate-checker' );

const HTML_SNIPPET = `
  <div class="rate-checker"></div>
`;

describe( 'explore-rates/rate-checker', () => {
  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
  } );

  describe( 'init()', () => {

    it( 'should not initialize when rate-checker class isn\'t found', () => {
      document.body.innerHTML = '';
      expect( rateChecker.init() ).toBe( false );
    } );

    it( 'should initialize when rate-checker class is found', () => {
      expect( rateChecker.init() ).toBe( true );
    } );

  } );
} );
