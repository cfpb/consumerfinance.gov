'use strict';

/**
 * @param {string} name - URL parameter name.
 * @returns {string|null} Decoded URI parameter.
 */
this.getURLParameter = function( name ) {
  var search = '[?|&]' + name + '=([^&;]+?)(&|#|;|$)';
  var regex = new RegExp( search ).exec( location.search ) || [ '', '' ];
  var uri = regex[1].replace( /\+/g, '%20' );
  return decodeURIComponent( uri ) || null;
};
