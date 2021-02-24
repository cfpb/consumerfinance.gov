const BASE_JS_PATH = '../../../../../../cfgov/unprocessed/apps/owning-a-home/';
const domLoader = require( BASE_JS_PATH + 'js/explore-rates/data-loader' );

// Mock the XmlHttpRequest call from axios.
import
axios
  from '../../../../../../cfgov/unprocessed/apps/owning-a-home/node_modules/axios';
jest.mock(
  '../../../../../../cfgov/unprocessed/apps/owning-a-home/node_modules/axios'
);
const mockResp = { data: 'mock data' };
axios.get.mockImplementation( () => Promise.resolve( mockResp ) );
jest.spyOn( axios, 'get' );

describe( 'explore-rates/data-loader', () => {

  describe( 'getLastCancelToken()', () => {
    it( 'should have constructed a CancelToken instance after calling getData',
      () => {
        expect( domLoader.getLastCancelToken() ).toBeUndefined();
        domLoader.getData();
        const cancelToken = domLoader.getLastCancelToken();
        expect( cancelToken ).toBeInstanceOf( axios.CancelToken );
      }
    );
  } );

  describe( 'getData()', () => {
    it( 'should call data API with correct query', () => {
      const today = new Date();
      const decache = String( today.getDate() ) + today.getMonth();
      domLoader.getData();
      return expect( axios.get ).toHaveBeenCalledWith(
        '/oah-api/rates/rate-checker',
        {
          params: {
            decache: decache,
            cancelToken: domLoader.getLastCancelToken()
          }
        }
      );
    } );
  } );

  describe( 'getCounties()', () => {
    it( 'should call county API with correct state query', () => {
      domLoader.getCounties( 'AL' );
      return expect( axios.get ).toHaveBeenCalledWith(
        '/oah-api/county/',
        { params: { state: 'AL' }}
      );
    } );
  } );
} );
