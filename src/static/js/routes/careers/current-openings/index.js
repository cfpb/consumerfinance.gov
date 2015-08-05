/* ==========================================================================
   Scripts for `/careers/current-openings/.
   ========================================================================== */

'use strict';

var simpleTableRowLinks = require( '../../../modules/simple-table-row-links' );

function init() {

  // TODO: Remove this when per-page JS is introduced.
  if ( document.querySelectorAll( '.careers-current-openings' ).length === 0 ) {
    return;
  }

  simpleTableRowLinks.init();
}

module.exports = { init: init };
