import { createChart } from 'cfpb-chart-builder'

const el = document.getElementById( 'landing-map' );
const dataUrl = "https://files.consumerfinance.gov/ccdb/hero-map-3y.json"

const chart = createChart( {
  el: el,
  source: dataUrl,
  colors: [
    'rgba(247, 248, 249, 0.5)',
    'rgba(212, 231, 230, 0.5)',
    'rgba(180, 210, 209, 0.5)',
    'rgba(137, 182, 181, 0.5)',
    'rgba(86, 149, 148, 0.5)',
    'rgba(37, 116, 115, 0.5)'
  ],
  type: 'tile_map'
} );
