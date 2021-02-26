const BASE_JS_PATH = '../../../../../cfgov/unprocessed/apps/';
const utils = require(
  BASE_JS_PATH + 'teachers-digital-platform/js/search-utils.js'
);

describe( 'The TDP search utils', () => {

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
    let url = utils.buildSearchResultsURL( 'foo', 'bar' );
    expect( url ).toEqual( 'foo?bar' );
    url = utils.buildSearchResultsURL( 'foo', 'bar', { partial: true } );
    expect( url ).toEqual( 'foo?bar&partial' );
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
    expect( searchError.msg )
      .toEqual( 'Your query returned zero results.' );
    const cancelError = utils.handleError( 0 );
    expect( cancelError.msg )
      .toEqual( 'Search request was cancelled.' );
    const unknownError = utils.handleError();
    expect( unknownError.msg )
      .toEqual( 'Sorry, our search engine is temporarily down.' );
  } );

  it( 'should replace the browser history', () => {
    const rs = global.history.replaceState = jest.fn();
    expect( rs.mock.calls.length ).toEqual( 0 );

    utils.updateUrl( 'foo', 'bar' );
    expect( rs.mock.calls.length ).toEqual( 1 );
    expect( rs.mock.calls[0] ).toEqual( [ null, null, 'foo?bar' ] );

    utils.updateUrl(
      '/teach/activities/', 'building_block=1&topic=3&q=executive'
    );
    expect( rs.mock.calls.length ).toEqual( 2 );
    expect( rs.mock.calls[1] ).toEqual(
      [
        null,
        null,
        '/teach/activities/?building_block=1&topic=3&q=executive'
      ]
    );
  } );

} );
