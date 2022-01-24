/* eslint-disable camelcase, no-shadow */

// Define string templates and constants
const county = ( { complete_fips, gse_limit, fha_limit, va_limit, county } ) => `<option value="${ complete_fips }" data-gse="${ gse_limit }" data-fha="${ fha_limit }" data-va="${ va_limit }">${ county }</option>`;

const chartTooltip = ( { y, key } ) => `<div class="chart-tooltip"><strong class="lenders">${ y }</strong><span class="text">lender${ y === 1 ? ' is' : 's are' } offering <br> rates at <strong>${ key }</strong>.</span></div>`;

const countyConfWarning = 'Based on your loan amount, you may not be eligible for a regular (conforming) conventional loan. Please enter your county so we can find the right loan type for you and get you the most accurate rates.';
const countyFHAWarning = 'Based on your loan amount, you may not be eligible for a regular FHA loan. Please enter your county so we can find the right loan type for you and get you the most accurate rates.';
const countyVAWarning = 'Based on your loan amount, you may not be eligible for a regular VA loan. Please enter your county so we can find the right loan type for you and get you the most accurate rates.';
const countyGenWarning = 'Please enter your county so we can check what loan types are available at your loan amount and get you the most accurate rates.';

export {
  county,
  countyConfWarning,
  countyFHAWarning,
  countyVAWarning,
  countyGenWarning,
  chartTooltip
};
