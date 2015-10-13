/* ==========================================================================
   Initialize Chosen.js
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );
require( 'chosen' );

/**
 * Initialize chosen jquery plugin.
 */
function init() {
  $( '.chosen-select' ).chosen( {
    width:           '100%',
    /* eslint-disable camelcase, lines-around-comment */
    no_results_text: 'Oops, nothing found!'
    /* eslint-endable */
  } );
}

// Expose public methods.
module.exports = { init: init };
