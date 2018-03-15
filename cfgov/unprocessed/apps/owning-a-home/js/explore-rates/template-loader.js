const TEMPLATE_DIR = '../../templates/explore-rates/';

// Load our handlebar templates.
const county = require( TEMPLATE_DIR + 'county-option.hbs' );
const countyConfWarning = require( TEMPLATE_DIR + 'county-conf-warning.hbs' );
const countyFHAWarning = require( TEMPLATE_DIR + 'county-fha-warning.hbs' );
const countyVAWarning = require( TEMPLATE_DIR + 'county-va-warning.hbs' );
const countyGenWarning = require( TEMPLATE_DIR + 'county-general-warning.hbs' );
const sliderLabel = require( TEMPLATE_DIR + 'slider-range-label.hbs' );
const creditAlert = require( TEMPLATE_DIR + 'credit-alert.hbs' );
const resultAlert = require( TEMPLATE_DIR + 'result-alert.hbs' );
const failAlert = require( TEMPLATE_DIR + 'fail-alert.hbs' );
const dpWarning = require( TEMPLATE_DIR + 'down-payment-warning.hbs' );
const chartTooltipSingle = require( TEMPLATE_DIR + 'chart-tooltip-single.hbs' );
const chartTooltipMultiple =
  require( TEMPLATE_DIR + 'chart-tooltip-multiple.hbs' );

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
