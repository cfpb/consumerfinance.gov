const BASE_JS_PATH = '../../../../../../cfgov/unprocessed/apps/owning-a-home/';
const domLoader = require( BASE_JS_PATH + 'js/explore-rates/data-loader' );

const mockResp = { data: 'mock data' };

global.fetch = jest.fn( () => Promise.resolve( {
  json: () => Promise.resolve( mockResp )
} )
);

describe( 'explore-rates/data-loader', () => {

  describe( 'getData()', () => {
    it( 'should call data API with correct query', () => {
      domLoader.getData( { a: 'b', c: 'd' } );
      return expect( fetch.mock.calls[0][0] ).toBe(
        '/oah-api/rates/rate-checker?a=b&c=d'
      );
    } );
  } );

  describe( 'getCounties()', () => {
    it( 'should call county API with correct state query', () => {
      domLoader.getCounties( 'AL' );
      return expect( fetch ).toHaveBeenCalledWith(
        '/oah-api/county/?state=AL'
      );
    } );
  } );
} );
