import Chart from '../../../../../cfgov/unprocessed/apps/ccdb-landing-map/js/Chart.js';

const HTML_SNIPPET = `
  <div id="map"></div>
`;
let element;

describe( 'chart constructor', () => {
  beforeEach( () => {

    // Empty HTML element for the chart.
    document.body.innerHTML = HTML_SNIPPET;
    element = document.querySelector( '#map' );

    // Mock highcharts required APIs.
    window.SVGElement.prototype.getBBox = () => ( {
      x: 0,
      y: 0
      // whatever other props you need
    } );

    // Mock window.fetch.
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
    console.log( 'element', element )
    const options = {
      source: 'https://foobar.json',
      isPerCapita: false,
      el: element
    };
    // eslint-disable-next-line no-unused-vars
    const chart = new Chart( options );
  } );

  it( 'builds per capita chart', () => {
    const options = {
      source: 'https://foobar.json',
      isPerCapita: true,
      el: element
    };
    // eslint-disable-next-line no-unused-vars
    const chart = new Chart( options );
  } );
} );
