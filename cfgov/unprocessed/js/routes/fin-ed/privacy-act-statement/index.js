/* ==========================================================================
   Scripts for `/fin-ed/privacy-act-statement/.
   ========================================================================== */

const atomicHelpers = require( '../../../modules/util/atomic-helpers' );
const Expandable = require( '../../../organisms/Expandable' );
const expandable = new Expandable( document.querySelector(
  '.o-secondary-navigation .o-expandable'
) );
expandable.init();
