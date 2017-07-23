'use strict';

var _UUID = 0;

/**
 * @returns {number} A Universal Unique Identifier.
 */
this.generateIdentifier = function() {
  var UUID = _UUID++;

  // Perhaps this is overkill.
  if ( _UUID === Number.MAX_VALUE ) {
    throw new Error( 'Maximum number of instances created!' );
  }

  return UUID;
};
