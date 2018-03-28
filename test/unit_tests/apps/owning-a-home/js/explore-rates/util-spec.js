const BASE_JS_PATH = '../../../../../../cfgov/unprocessed/apps/owning-a-home/';
const util = require( BASE_JS_PATH + 'js/explore-rates/util' );

const HTML_SNIPPET = `
  <strong id="timestamp"></strong>
`;

let timeStampDom;

describe( 'explore-rates/util', () => {
  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
    timeStampDom = document.querySelectorAll( '#timestamp' );
  } );

  describe( 'formatTimestampMMddyyyy()', () => {
    it( 'should format a timestamp as a date.', () => {
      expect( util.formatTimestampMMddyyyy( '2018-03-14T04:00:00Z' ) )
        .toBe( '03/14/2018' );
    } );
  } );

  describe( 'renderDatestamp()', () => {
    it( 'should format a timestamp as a date.', () => {
      util.renderDatestamp( timeStampDom, '2018-03-14T04:00:00Z' );
      expect( timeStampDom.textContent ).toBe( '03/14/2018' );
    } );
  } );
} );
