import * as analyticsUtil from '../../../../../../cfgov/unprocessed/apps/analytics-gtm/js/util/analytics-util';

const HTML_SNIPPET = `
  <div id="test-elem"></div>
`;

describe( 'analytics-util', () => {
  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
  } );

  describe( 'hostsAreEqual()', () => {
    it( 'should return true if hosts are equal', () => {
      const host1 = 'https://www.example.com';
      const host2 = 'https://www.example.com';
      expect( analyticsUtil.hostsAreEqual( host1, host2 ) ).toBe( true );
    } );

    it( 'should return false if hosts are NOT equal', () => {
      const host1 = 'https://www.github.com';
      const host2 = 'https://www.github.io';
      expect( analyticsUtil.hostsAreEqual( host1, host2 ) ).toBe( false );
    } );
  } );
} );
