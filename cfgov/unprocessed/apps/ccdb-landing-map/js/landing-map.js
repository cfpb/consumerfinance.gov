import Chart from './Chart';
import debounce from 'debounce';

let perCapBtn, rawBtn,
    isPerCapita = false;

/**
 * Wrapper function around the chart cleanup and chart initialization
 */
function start() {
  const el = document.getElementById( 'landing-map' );
  const elements = el.querySelectorAll( '*' );
  for ( let i = 0; i < elements.length; i++ ) {
    const node = elements[i];
    node.parentNode.removeChild( node );
  }

  const dataUrl = 'https://files.consumerfinance.gov/ccdb/hero-map-3y.json';
  // eslint-disable-next-line no-unused-vars
  const chart = new Chart( {
    el: el,
    source: dataUrl,
    isPerCapita
  } );
}

/**
 * main entrypoint into landing map page, init the buttons, kick off map
 */
function init() {
  perCapBtn = document.getElementsByClassName( 'capita' )[0];
  rawBtn = document.getElementsByClassName( 'raw' )[0];

  perCapBtn.onclick = () => {
    perCapBtn.classList.add( 'selected' );
    rawBtn.classList.remove( 'selected' );
    isPerCapita = true;
    start();
  };

  rawBtn.onclick = () => {
    rawBtn.classList.add( 'selected' );
    perCapBtn.classList.remove( 'selected' );
    isPerCapita = false;
    start();
  };

  window.addEventListener( 'resize', debounce( function() {
    start();
  }, 200 ) );

  start();
}

export default { init };
