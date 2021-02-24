const BASE_JS_PATH = '../../../../../cfgov/unprocessed/apps/regulations3k';

const utils = require( `${ BASE_JS_PATH }/js/regs3k-utils.js` );

describe( 'The Regs3K search utils', () => {

  describe( 'AJAX utils', () => {

    it( 'should fetch a resource', done => {
      const mockXHR = {
        open: jest.fn(),
        send: jest.fn(),
        readyState: 4,
        status: 200,
        onreadystatechange: jest.fn(),
        responseText: [
          { searchResult: 'one' },
          { anotherSearchResult: 'two' }
        ]
      };
      global.XMLHttpRequest = jest.fn( () => mockXHR );
      utils.fetch( 'api/search', ( err, data ) => {
        expect( err ).toEqual( null );
        expect( data ).toEqual(
          [ { searchResult: 'one' }, { anotherSearchResult: 'two' } ]
        );
        done();
      } );
      mockXHR.onreadystatechange();
    } );

    it( 'should fail to fetch a resource', done => {
      const mockXHR = {
        open: jest.fn(),
        send: jest.fn(),
        readyState: 4,
        status: 404,
        onreadystatechange: jest.fn(),
        responseText: 'Server error!'
      };
      global.XMLHttpRequest = jest.fn( () => mockXHR );
      utils.fetch( 'api/search', err => {
        expect( err ).toEqual( 404 );
        done();
      } );
      mockXHR.onreadystatechange();
    } );

  } );

  describe( 'Hash utils', () => {

    it( 'should convert a hash', () => {
      expect( utils.getNewHash( '1010-Interp-1' ) ).toEqual( 'Interp-1' );
      expect( utils.getNewHash( '#1010-Interp-1' ) ).toEqual( 'Interp-1' );

      expect( utils.getNewHash( '1011-4-a' ) ).toEqual( 'a' );
      expect( utils.getNewHash( '#1011-4-a' ) ).toEqual( 'a' );

      expect( utils.getNewHash( '1003-2-f-Interp-3' ) )
        .toEqual( '2-f-Interp-3' );
      expect( utils.getNewHash( '#1003-2-f-Interp-3' ) )
        .toEqual( '2-f-Interp-3' );

      expect( utils.getNewHash( '1003-4-a-9-ii-C' ) ).toEqual( 'a-9-ii-C' );
      expect( utils.getNewHash( '#1003-4-a-9-ii-C' ) ).toEqual( 'a-9-ii-C' );
    } );

    it( 'should check if a hash needs to be converted', () => {
      expect( utils.isOldHash( '1010-Interp-1' ) ).toBeTrue;
      expect( utils.isOldHash( '#1010-Interp-1' ) ).toBeTrue;

      expect( utils.isOldHash( '101-Interp-1' ) ).toBeFalse;
      expect( utils.isOldHash( '#101-Interp-1' ) ).toBeFalse;

      expect( utils.isOldHash( '1003-2-f-Interp-3' ) ).toBeTrue;
      expect( utils.isOldHash( '#1003-2-f-Interp-3' ) ).toBeTrue;

      expect( utils.isOldHash( '003-2-f-Interp-3' ) ).toBeFalse;
      expect( utils.isOldHash( '#003-2-f-Interp-3' ) ).toBeFalse;

      expect( utils.isOldHash( 'bloop' ) ).toBeFalse;
      expect( utils.isOldHash( '#bloop' ) ).toBeFalse;

      expect( utils.isOldHash( 'asdf-2-f-Interp-3' ) ).toBeFalse;
      expect( utils.isOldHash( '#asdf-2-f-Interp-3' ) ).toBeFalse;
    } );

  } );

} );
