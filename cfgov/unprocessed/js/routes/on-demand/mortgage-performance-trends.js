/* ==========================================================================
   Mortgage Performance Trends
   Scripts for `/data-research/mortgage-performance-trends/`.
   ========================================================================== */

/* To aid debugging, uncomment the below line.
   It will enable console logging of state changes (except in IE).
   window.MP_DEBUG = window.navigator.userAgent.indexOf('MSIE ') === -1; */

/* CFPB's charting library looks for data files on S3 by default.
   MP uses a custom API so point our charts to it instead. */
window.CFPB_CHART_DATA_SOURCE_BASE = '/data-research/mortgages/api/v1/';

import { Chart, Map } from '../../organisms/MortgagePerformanceTrends';

new Chart({ container: 'mp-line-chart-container' });
new Map({ container: 'mp-map-container' });
