import 'regenerator-runtime/runtime';
import
Chart
  from '../../../../../cfgov/unprocessed/apps/ccdb-landing-map/js/Chart';

describe( 'chart constructor', () => {
  beforeEach( () => {
    global.fetch = jest.fn().mockImplementation( url => {
      expect( url ).toEqual( 'https://foobar.json' );
      return new Promise( resolve => {
        resolve( {
          json: function() {
            return [
              { name: 'AK', fullName: 'Alaska', value: 713, issue: 'A', product: 'B', perCapita: 0.9653855787913047 },
              { name: 'AL', fullName: 'Alabama', value: 10380, issue: 'A', product: 'B', perCapita: 2.139866013052358 },
              { name: 'AR', fullName: 'Arkansas', value: 4402, issue: 'A', product: 'B', perCapita: 1.4782010675821977 },
              { name: 'AZ', fullName: 'Arizona', value: 14708, issue: 'A', product: 'B', perCapita: 2.159782177421084 }
            ];
          }
        } );
      } );
    } );
  } );

  it( 'builds raw chart', () => {
    const options = {
      source: 'https://foobar.json',
      isPerCapita: false
    };
    // eslint-disable-next-line no-unused-vars
    const chart = new Chart( options );
  } );

  it( 'builds per capita chart', () => {
    const options = {
      source: 'https://foobar.json',
      isPerCapita: true
    };
    // eslint-disable-next-line no-unused-vars
    const chart = new Chart( options );
  } );
} );
