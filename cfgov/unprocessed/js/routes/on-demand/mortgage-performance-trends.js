
/* ==========================================================================
   Mortgage Performance Trends
   Scripts for `/data-research/mortgage-performance-trends/`.
   ========================================================================== */

'use strict';

// Enable console logging of state changes.
// TODO: Set to false before release.
window.MP_DEBUG = true;

// CFPB's charting library looks for data files on S3 by default.
// MP uses a custom API so point our charts to it instead.
window.CFPB_CHART_DATA_SOURCE_BASE = '/data-research/mortgages/api/v1/';

const MortgagePerformanceTrends = require( '../../organisms/MortgagePerformanceTrends' );

const chart = new MortgagePerformanceTrends.Chart( { container: 'mp-line-chart-container' } );
const map = new MortgagePerformanceTrends.Map( { container: 'mp-map-container' } );

// Expose charts to aid debugging while in development.
// TODO: Remove before release.
window.CFPB_CHART_DEBUG = {
  chart,
  map
}
