import TileMap from './TileMap.js';

/**
 *  Chart class
 *  Replace the functionality in cfpb-chart-builder/src/js/index.js
 */
class Chart {

  constructor( chartOptions ) {
    this.chartOptions = chartOptions;

    // console.log('rload')
    fetch( chartOptions.source )
    .then( response=> {
      return response.json();
    })
    .then( data => {
      this.chartOptions.data = data;
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


document.getElementsByClassName('per-capita')[0].onclick = function(){
  // probably need to set some variable somewhere and redraw the map with filtered data.
  start();
}

start();

