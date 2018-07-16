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

  it( 'should show an element loading', () => {
    let el = { style: { opacity: 1 }};
    el = utils.showLoading( el );
    expect( el.style.opacity ).toEqual( 0.5 );
  } );

  it( 'should stop an element loading', () => {
    let el = { style: { opacity: 0.5 }};
    el = utils.hideLoading( el );
    expect( el.style.opacity ).toEqual( 1 );
  } );

  it( 'should clear a checkbox', () => {
    const checkbox = utils.clearCheckbox( { checked: true } );
    expect( checkbox.checked ).toBeFalsy();
  } );

  it( 'should handle errors', () => {
    const searchError = utils.handleError( 'no-results' );
    expect( searchError.msg ).toEqual( 'Your query returned zero results.' );
    const unknownError = utils.handleError();
    expect( unknownError.msg ).toEqual( 'Sorry, our search engine is temporarily down.' );
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

  it( 'should replace the browser history', () => {
    const rs = global.history.replaceState = jest.fn();
    expect( rs.mock.calls.length ).toEqual( 0 );

    utils.updateUrl( 'foo', 'bar' );
    expect( rs.mock.calls.length ).toEqual( 1 );
    expect( rs.mock.calls[0] ).toEqual( [ null, null, 'foo?bar' ] );

    utils.updateUrl( '/regulations/search/', 'regs=1002&regs=1010&q=funding' );
    expect( rs.mock.calls.length ).toEqual( 2 );
    expect( rs.mock.calls[1] ).toEqual( [ null, null, '/regulations/search/?regs=1002&regs=1010&q=funding' ] );
  } );

} );
