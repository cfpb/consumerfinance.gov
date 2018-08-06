const BASE_JS_PATH = '../../../../../cfgov/unprocessed/apps/regulations3k';

const { fetch } = require( `${ BASE_JS_PATH }/js/regs3k-utils.js` );

describe( 'The Regs3K search utils', () => {

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
    fetch( 'api/search', ( err, data ) => {
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
    fetch( 'api/search', err => {
      expect( err ).toEqual( 404 );
      done();
    } );
    mockXHR.onreadystatechange();
  } );

} );
