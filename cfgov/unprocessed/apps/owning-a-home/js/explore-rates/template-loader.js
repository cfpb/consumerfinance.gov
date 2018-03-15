

// Load our handlebar templates.
const county = require( 'Templates/county-option.hbs' );
const countyConfWarning = require(  'Templates/county-conf-warning.hbs' );
const countyFHAWarning = require( 'Templates/county-fha-warning.hbs' );
const countyVAWarning = require( 'Templates/county-va-warning.hbs' );
const countyGenWarning = require( 'Templates/county-general-warning.hbs' );
const sliderLabel = require( 'Templates/slider-range-label.hbs' );
const creditAlert = require( 'Templates/credit-alert.hbs' );
const resultAlert = require( 'Templates/result-alert.hbs' );
const failAlert = require( 'Templates/fail-alert.hbs' );
const dpWarning = require( 'Templates/down-payment-warning.hbs' );
const chartTooltipSingle = require( 'Templates/chart-tooltip-single.hbs' );
const chartTooltipMultiple = require( 'Templates/chart-tooltip-multiple.hbs' );

module.exports = {
  county,
  countyConfWarning,
  countyFHAWarning,
  countyVAWarning,
  countyGenWarning,
  sliderLabel,
  creditAlert,
  resultAlert,
  failAlert,
  dpWarning,
  chartTooltipSingle,
  chartTooltipMultiple
};
