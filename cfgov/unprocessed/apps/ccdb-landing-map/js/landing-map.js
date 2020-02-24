import TileMap from './TileMap.js';

/**
 *  Chart class
 *  Replace the functionality in cfpb-chart-builder/src/js/index.js
 */
class Chart {
  constructor( chartOptions ) {
    this.chartOptions = chartOptions;

    fetch( chartOptions.source )
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

/**
 * main function to draw a new map.
 * @param {boolean} isPerCapita display per capita complaints (decimals)
 */
function start( isPerCapita ) {
  const el = document.getElementById( 'landing-map' );
  el.querySelectorAll( '*' ).forEach( n => n.remove() );

  const dataUrl = 'https://files.consumerfinance.gov/ccdb/hero-map-3y.json';
  // eslint-disable-next-line no-unused-vars
  const chart = new Chart( {
    el: el,
    source: dataUrl,
    isPerCapita
  } );
}

const perCapBtn = document.getElementsByClassName( 'capita' )[0];
const rawBtn = document.getElementsByClassName( 'raw' )[0];

perCapBtn.onclick = () => {
  perCapBtn.classList.add( 'selected' );
  rawBtn.classList.remove( 'selected' );
  start( true );
};

rawBtn.onclick = () => {
  rawBtn.classList.add( 'selected' );
  perCapBtn.classList.remove( 'selected' );
  start( false );
};

start( false );

