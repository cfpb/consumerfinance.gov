const utils = require( '../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/utils.js' );

describe( 'The TDP search utils', () => {

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
      utils.fetch( 'activities', ( err, data ) => {
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
      utils.fetch( 'activities', err => {
        expect( err ).toEqual( 404 );
        done();
      } );
      mockXHR.onreadystatechange();
    } );

  } );

} );
