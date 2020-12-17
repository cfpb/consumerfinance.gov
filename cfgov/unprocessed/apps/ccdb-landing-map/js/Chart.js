import 'whatwg-fetch';
import TileMap from './TileMap';

/**
 *  Chart class
 *  Replace the functionality in cfpb-chart-builder/src/js/index.js
 */
export default class Chart {
  constructor( chartOptions ) {
    this.chartOptions = chartOptions;

    window.fetch( chartOptions.source )
      .then( response => response.json() )
      .then( data => {
        data = data.map( o => {
          const perCapita = parseFloat( o.perCapita.toFixed( 2 ) );
          const displayValue = this.chartOptions.isPerCapita ?
            perCapita : o.value;
          return {
            ...o,
            displayValue,
            perCapita
          };
        } );

        this.chartOptions.data = data;
        this.draw( this.chartOptions );
      } );
  }

  draw( chartOptions ) {
    this.highchart = new TileMap( chartOptions );
  }
}
