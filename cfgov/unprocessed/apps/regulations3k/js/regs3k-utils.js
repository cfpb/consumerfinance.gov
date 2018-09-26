import { ajaxRequest as xhr } from '../../../js/modules/util/ajax-request';

/**
 * fetch - Wrapper for our ajax request method with callback support
 *
 * @param {string} url URL to request
 * @param {function} cb  Success/failure callback
 *
 * @returns {object} XMLHttpRequest object
 */
const fetch = ( url, cb ) => xhr( 'GET', url, {
  success: data => cb( null, data ),
  fail: err => cb( err )
} );

/**
 * getNewHash - Convert an old eRegs hash into a Regs3K hash.
 *
 * @param {string} hash Old eRegs URL hash
 *
 * @returns {string} New Regs3K hash
 */
const getNewHash = hash => {
  if ( ( /(\w+-)+Interp-/ ).test( hash ) ) {
    // Trim off DDDD- e.g. 1003-2-f-Interp-3 becomes 2-f-Interp-3
    return hash.replace( /^#?\d\d\d\d-/, '' );
  }
  // Trim off DDDD-D- e.g. 1003-4-a-9-ii-C becomes a-9-ii-C
  return hash.replace( /^#?\d\d\d\d-\w+-/, '' );
};


/**
 * isOldHash - Check if provided hash is from the old eRegs site
 * All the former eRegs paragraph markers start with their four-digit reg.
 *
 * @param {string} hash URL hash
 *
 * @returns {boolean} true/false
 */
const isOldHash = hash => ( /^#?\d\d\d\d/ ).test( hash );

module.exports = {
  fetch,
  getNewHash,
  isOldHash
};
