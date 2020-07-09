const xhr = require( '../../../js/modules/util/ajax-request' ).ajaxRequest;

/**
 * fetch - Wrapper for our ajax request method with callback support
 *
 * @param {string} url URL to request
 * @param {function} cb  Success/failure callback
 */
function fetch( url, cb ) {
  xhr( 'GET', url, {
    success: data => cb( null, data ),
    fail: err => cb( err )
  } );
}

module.exports = {
  fetch: fetch
};
