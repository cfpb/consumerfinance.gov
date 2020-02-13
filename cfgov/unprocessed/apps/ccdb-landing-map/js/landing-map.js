import TileMap from './TileMap.js';
import getData from 'cfpb-chart-builder/src/js/utils/get-data';

// -----------------------------------------------------------------------------
// Replace the functionality in cfpb-chart-builder/src/js/index.js

class Chart {

  constructor( chartOptions ) {
    this.chartOptions = chartOptions;
    getData( chartOptions.source ).then( data => {
      this.chartOptions.data = data;
      this.draw( this.chartOptions );
    } );
  }

  draw( chartOptions ) {
    this.highchart = new TileMap( chartOptions );
  }
}

// -----------------------------------------------------------------------------
// Main

const el = document.getElementById( 'landing-map' );
const dataUrl = "https://files.consumerfinance.gov/ccdb/hero-map-3y.json"

const chart = new Chart( {
  el: el,
  source: dataUrl,
  title: 'Complaints by State',
  description: 'The complaints by state for...'
} );
