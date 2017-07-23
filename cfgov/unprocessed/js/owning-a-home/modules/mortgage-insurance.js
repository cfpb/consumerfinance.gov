'use strict';

var $ = require( 'jquery' );
var config = require( '../../../../config/config.json' );

// TODO: Consolidate with rates.js.
/**
 * Get data from the API.
 * @param  {object} params Hash of request params.
 * Should include: price, loan_amount, minfico, maxfico,
 * rate_structure, loan_term, loan_type, arm_type,
 * va_status, va_first_use
 * @returns {object} jQuery promise.
 */
function fetch( params ) {
  var today = new Date();
  var decache = String( today.getDate() ) + today.getMonth();

  return $.ajax( {
    type:        'GET',
    url:         config.mortgageInsuranceAPI,
    data:        $.extend( { decache: decache }, params ),
    dataType:    'json',
    contentType: 'application/json'
  } );

}

module.exports = fetch;
