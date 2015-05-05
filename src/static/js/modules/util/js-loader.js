/* ==========================================================================
   Dynamic Nonblocking script loader.
   ========================================================================== */

'use strict';

// Dynamically attach and load a script tag in the head of the page.
// @param url {String} The URL of the script to load.
// @param callback {Function} (Optional) a function to call when done.
function loadScript( url, callback ) {
  var script = document.createElement( 'script' );
  script.type = 'text/javascript';

  // Handle Internet Explorer
  if ( script.readyState ) {
    script.onreadystatechange = function() {
      if ( script.readyState === 'loaded' || script.readyState === 'complete' ) {
        script.onreadystatechange = null;
        if ( callback ) callback();
      }
    };
  // Other browsers.
  } else {
    script.onload = function() {
      if ( callback ) callback();
    };
  }

  script.src = url;
  document.getElementsByTagName( 'head' )[0].appendChild( script );
}

// Expose public methods.
module.exports = { loadScript: loadScript };
