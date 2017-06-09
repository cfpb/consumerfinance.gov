'use strict';

/**
* Initiates an ajax request when passed a type, url,
* and an optional opts object.
*
* @param {string} type request type (GET, POST)
* @param {string} url request url
* @param {Object} opts object containing optional
* request parameters, including data, headers,
* and success, fail, and done callbacks
* @returns {Object} xhr
*/

function ajaxRequest( type, url, opts ) {
  var DONE_CODE = 4;
  var SUCCESS_CODES = {
    200: 'ok',
    201: 'created',
    202: 'accepted',
    203: 'non-authoritative info',
    204: 'no content',
    205: 'reset content',
    206: 'partial content'
  };
  var xhr = new XMLHttpRequest();
  xhr.open( type, url );
  if ( opts.headers ) {
    opts.headers.forEach( function( header ) {
      xhr.setRequestHeader( header[0], header[1] );
    } );
  }
  xhr.onreadystatechange = function() {
    if ( xhr.readyState === DONE_CODE ) {
      if ( xhr.status in SUCCESS_CODES ) {
        if ( typeof opts.success === 'function' ) opts.success();
      } else if ( typeof opts.fail === 'function' ) {
        opts.fail();
      }
      if ( typeof opts.done === 'function' ) opts.done();
    }
  };
  xhr.send();
  return xhr;
}

module.exports = {
  ajaxRequest: ajaxRequest
};
