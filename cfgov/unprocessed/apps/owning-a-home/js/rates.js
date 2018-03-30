const $ = require( 'jquery' );
const config = require( '../config.json' );

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
  const today = new Date();
  const decache = String( today.getDate() ) + today.getMonth();

  return $.ajax( {
    type:        'GET',
    url:         config.rateCheckerAPI,
    data:        $.extend( { decache: decache }, params ),
    dataType:    'json',
    contentType: 'application/json'
  } );
}

module.exports = fetch;
