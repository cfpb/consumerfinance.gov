/* ==========================================================================
   Utilities
   ========================================================================== */

'use strict';

// Based on http://css-tricks.com/snippets/javascript/get-url-variables/ and
// added optional second argument.
function getQueryVariable( key, queryString ) {
  var query;
  var vars;

  if ( typeof queryString === 'string' ) {
    query = queryString;
  } else {
    query = window.location.search.substring( 1 );
  }

  vars = query.split( '&' );

  for ( var i = 0; i < vars.length; i++ ) {
    var pair = vars[i].split( '=' );
    if ( pair[0] === key ) {
      return pair[1];
    }
  }

  return false;
}

function replaceQueryVariable( key, value, queryString ) {
  var query;
  var vars;

  if ( typeof queryString === 'string' ) {
    query = queryString;
  } else if ( window.location.search.charAt( 0 ) === '?' ) {
    query = window.location.search.substring( 1 );
  } else {
    query = window.location.search;
  }

  vars = query.split('&');

  var pair;
  for ( var i = 0; i < vars.length; i++ ) {
    pair = vars[i].split( '=' );
    if ( pair[0] === key ) {
      return '?' + query.replace(
        pair[0] + '=' + pair[1],
        pair[0] + '=' + value
      );
    }
  }

  return false;
}

function getQuery() {
  if ( window.location.search.charAt(0) === '' ) {
    return false;
  }
  return window.location.search;
}

// Expose public methods.
module.exports = {
  getQueryVariable:     getQueryVariable,
  replaceQueryVariable: replaceQueryVariable,
  getQuery:             getQuery
};
