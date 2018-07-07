const BASE_JS_PATH = '../../../../../cfgov/unprocessed/apps/regulations3k';

const utils = require( `${ BASE_JS_PATH }/js/search-utils.js` );

describe( 'The Regs3K search utils', () => {

  it( 'should get values from search form fields', () => {
    const searchEl = {
      name: 'foo',
      value: 'bar'
    };
    const filterEls = [ {
      name: 'fizz',
      value: 'buzz'
    } ];
    const values = utils.getSearchValues( searchEl, filterEls );
    expect( values ).toEqual( [
      { foo: 'bar' },
      { fizz: 'buzz' }
    ] );
  } );

  it( 'should serialize form fields', () => {
    const serialized = utils.serializeFormFields( [
      { foo: 'bar' }
    ] );
    expect( serialized ).toEqual( 'foo=bar' );
  } );

  it( 'should build a search results URL', () => {
    const URL = utils.buildSearchResultsURL( 'foo', 'bar' );
    expect( URL ).toEqual( 'foo?bar&partial' );
  } );

  it( 'should fetch search results', done => {
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
    utils.fetchSearchResults( 'api/search', ( err, data ) => {
      expect( err ).toEqual( null );
      expect( data ).toEqual(
        [ { searchResult: 'one' }, { anotherSearchResult: 'two' } ]
      );
      done();
    } );
    mockXHR.onreadystatechange();
  } );

  it( 'should fail to fetch search results', done => {
    const mockXHR = {
      open: jest.fn(),
      send: jest.fn(),
      readyState: 4,
      status: 404,
      onreadystatechange: jest.fn(),
      responseText: 'Server error!'
    };
    global.XMLHttpRequest = jest.fn( () => mockXHR );
    utils.fetchSearchResults( 'api/search', err => {
      expect( err ).toEqual( 404 );
      done();
    } );
    mockXHR.onreadystatechange();
  } );

} );
