import { createChart } from 'cfpb-chart-builder'

// -----------------------------------------------------------------------------

const el = document.getElementById( 'landing-map' );
const dataUrl = "https://files.consumerfinance.gov/ccdb/hero-map-3y.json"

const chart = createChart( {
  el: el,
  source: dataUrl,
  type: 'tile_map'
} );
