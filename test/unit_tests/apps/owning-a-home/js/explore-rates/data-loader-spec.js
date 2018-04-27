const BASE_JS_PATH = '../../../../../../cfgov/unprocessed/apps/owning-a-home/';
const domLoader = require( BASE_JS_PATH + 'js/explore-rates/data-loader' );

const createXHRMock = require( '../../../../../util/mock-xhr' );
let xhrMock;

describe( 'explore-rates/data-loader', () => {
  beforeAll( () => {
    xhrMock = createXHRMock();
  } );

  describe( 'getData()', () => {
    it( 'should call data API with correct query', () => {
      domLoader.getData();

      expect( xhrMock.open ).toBeCalled();
      expect( xhrMock.send ).toBeCalled();
    } );
  } );

  describe( 'getCounties()', () => {
    it( 'should call county API with correct state query', () => {
      domLoader.getCounties( 'AL' );

      expect( xhrMock.open )
        .toBeCalledWith( 'GET', '/oah-api/county/?state=AL' );
      expect( xhrMock.send ).toBeCalled();
    } );
  } );
} );
