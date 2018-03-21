/* ==========================================================================
   Dynamic Nonblocking script loader.
   ========================================================================== */


/**
 * Dynamically attach and load a script tag in the head of the page.
 * @param {string} url The URL of the script to load.
 * @param {Function} callback (Optional) a function to call when done.
 */
function loadScript( url, callback ) {
  const script = document.createElement( 'script' );
  script.type = 'text/javascript';

  script.onload = function() {
    if ( callback ) {
      return callback();
    }
    return null;
  };

  script.src = url;
  document.getElementsByTagName( 'head' )[0].appendChild( script );
}

// Expose public methods.
module.exports = { loadScript: loadScript };
