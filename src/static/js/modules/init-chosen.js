/* ==========================================================================
   Initialize Chosen.js
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );
require( 'chosen' );

function init() {
  $( '.chosen-select' ).chosen( {
    width:           '100%',
    no_results_text: 'Oops, nothing found!'
  } );
}

// Expose public methods.
module.exports = { init: init };
