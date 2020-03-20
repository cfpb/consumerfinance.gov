import Chart from './Chart';

let idLink, perCapBtn, rawBtn;

/**
 * Wrapper function around the chart cleanup and chart initialization
 * @param {boolean} isPerCapita display per capita complaints (decimals)
 */
function start( isPerCapita ) {
  const el = document.getElementById( 'landing-map' );
  const elements = el.querySelectorAll( '*' )
  for ( let i = 0; i< elements.length; i++ ) {
    elements[i].remove();
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
  idLink = document.getElementById( 'all-results' );
  perCapBtn = document.getElementsByClassName( 'capita' )[0];
  rawBtn = document.getElementsByClassName( 'raw' )[0];

  perCapBtn.onclick = () => {
    perCapBtn.classList.add( 'selected' );
    rawBtn.classList.remove( 'selected' );
    let link = idLink.getAttribute( 'href' );
    link = link.replace( 'None', 'Per%201000%20pop.' );
    idLink.setAttribute( 'href', link );
    start( true );
  };

  rawBtn.onclick = () => {
    rawBtn.classList.add( 'selected' );
    perCapBtn.classList.remove( 'selected' );
    let link = idLink.getAttribute( 'href' );
    link = link.replace( 'Per%201000%20pop.', 'None' );
    idLink.setAttribute( 'href', link );

    start( false );
  };

  start( false );
}

export default { init };
