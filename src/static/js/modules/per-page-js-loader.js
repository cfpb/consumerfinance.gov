'use strict';

var jsManifest = require( '../config/js-manifest-config.js' );
var jsLoader = require( '../modules/util/js-loader' );

/**
 * Load a page-specific JavaScript dynamically into the header
 * if the page has a page-specific script available.
 */
function init() {
  var rawJson = document.getElementById( 'page-javascript' ).innerHTML;
  var json = JSON.parse( rawJson );
  var pageScriptUrl = json.routes[json.url];

  // If page script is not found,
  // walk up the directory structure looking for a template-level script
  // instead of a per-page script. If none is found continue.
  if ( !pageScriptUrl ) {
    var pathPieces = json.url.split( '/' );
    var newPath;

    while ( pathPieces.length > 0 && typeof pageScriptUrl === 'undefined' ) {
      pathPieces.pop();
      newPath = pathPieces.join( '/' ) + '/' + jsManifest.templateScriptName;
      pageScriptUrl = json.routes[newPath];
    }
  }

  if ( pageScriptUrl ) {
    jsLoader.loadScript( jsManifest.readPath + '/' + pageScriptUrl );
  }
}

module.exports = { init: init };
