'use strict';

var $ = require( '../node_modules/jquery' );
var config = require( '../config.json' );

// TODO: Consolidate with mortgage-insurance.js.
/**
 * Get data from the API.
 * @param  {Object} params
 *   Hash of request params.
 *   Should include: price, loan_amount, minfico, maxfico,
 *   state, rate_structure, loan_term, loan_type, arm_type
 * @returns {Object} jQuery promise.
 */
function fetch( params ) {
  var today = new Date();
  var decache = '' + today.getDate() + today.getMonth();

  return $.ajax( {
    type:        'GET',
    url:         config.rateCheckerAPI,
    data:        $.extend( { decache: decache }, params ),
    dataType:    'json',
    contentType: 'application/json'
  } );
}

module.exports = fetch;
