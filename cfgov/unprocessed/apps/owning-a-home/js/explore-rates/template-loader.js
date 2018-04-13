// Load our handlebar templates.
const county = require( '../../templates/county-option.hbs' );
const countyConfWarning = require( '../../templates/county-conf-warning.hbs' );
const countyFHAWarning = require( '../../templates/county-fha-warning.hbs' );
const countyVAWarning = require( '../../templates/county-va-warning.hbs' );
const countyGenWarning = require( '../../templates/county-general-warning.hbs' );
const chartTooltipSingle = require( '../../templates/chart-tooltip-single.hbs' );
const chartTooltipMultiple = require( '../../templates/chart-tooltip-multiple.hbs' );

module.exports = {
  county,
  countyConfWarning,
  countyFHAWarning,
  countyVAWarning,
  countyGenWarning,
  chartTooltipSingle,
  chartTooltipMultiple
};
