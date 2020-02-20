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
      data = data.map(o => {
        const perCapita = parseFloat(o.perCapita.toFixed(2));
        const displayValue = this.chartOptions.perCapita ? perCapita : o.value;
        return {
          ...o,
          displayValue,
          perCapita
        };
      });

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

function start(perCapita ) {
  const el = document.getElementById('landing-map');
  el.querySelectorAll('*').forEach(n => n.remove());

  const dataUrl = 'https://files.consumerfinance.gov/ccdb/hero-map-3y.json';
  // eslint-disable-next-line no-unused-vars
  const chart = new Chart({
    el: el,
    source: dataUrl,
    title: 'Complaints by State',
    description: 'The complaints by state for...',
    perCapita
  });
}


document.getElementsByClassName('capita')[0].onclick = () => {
  start(true);
};

document.getElementsByClassName('raw')[0].onclick = () => {
  start(false);
};

start( false );

