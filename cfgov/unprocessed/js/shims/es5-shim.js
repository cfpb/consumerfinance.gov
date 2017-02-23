/* ==========================================================================
   ES 5 Shim/Sham, added for BB7.
   ========================================================================== */

'use strict';

if ( window.Modernizr && window.Modernizr.es5 === false ) {
  // Global modules.
  require( 'es5-shim' ); // eslint-disable-line global-require
  require( 'es5-sham' ); // eslint-disable-line global-require
}
