/* ==========================================================================
   Quality Assurance Element
   ========================================================================== */

'use strict';

/**
 * Retrieves QA Protractor ElementFinder when provided
 * with the following params:
 *
 * @param {integer} selector - dom selector.
 * @param {boolean} getAllFlag - flag indicating wether to use element.all.
 * @returns {ElementFinder|ElementArrayFinder}
 * - Protractor ElementFinder or ElementFinder array.
 */
function get( selector, getAllFlag ) {
  var domQuery = getAllFlag ? element.all : element;

  return domQuery( by.css( '[data-qa-hook="' + selector + '"]' ) );
}

// Expose public methods.
module.exports = { get: get };
