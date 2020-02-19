import TileMap from './TileMap.js';

/**
 *  Chart class
 *  Replace the functionality in cfpb-chart-builder/src/js/index.js
 */
class Chart {

  constructor( chartOptions ) {
    this.chartOptions = chartOptions;
    fetch( chartOptions.source )
    .then( response=> {
      return response.json();
    })
    .then( data => {
      const mappedData = data.map(o => {
        // api needs to provide full state name
        o.fullName = 'State name here';
        return o;
      });

      this.chartOptions.data = [ mappedData ];
      this.draw( this.chartOptions );
    } );
  }

  draw( chartOptions ) {
    this.highchart = new TileMap( chartOptions );
  }
}

/**
 * main
 */

function start() {
  const el = document.getElementById('landing-map');
  const dataUrl = 'https://files.consumerfinance.gov/ccdb/hero-map-3y.json';
// eslint-disable-next-line no-unused-vars
  const chart = new Chart({
    el: el,
    source: dataUrl,
    title: 'Complaints by State',
    description: 'The complaints by state for...',
  });
}


document.getElementsByClassName('interval-All')[0].onclick = function(){
  // probably need to set some variable somewhere and redraw the map with filtered data.
  start();
}

start();

