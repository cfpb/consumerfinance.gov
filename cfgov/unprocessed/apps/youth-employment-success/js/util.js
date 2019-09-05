let UNDEFINED;

const INVALID_OBJECT_ERROR = 'The `entries` function must be passed an object as its first argument';

/**
 * Helper method to generate an action creator
 * @param {string} actionType The name of the action to be dispatched
 * @returns {function} Curried action creator function that accepts a
 *   data argument and returns an action
 */
function actionCreator( actionType ) {
  return function( data ) {
    return {
      type: actionType,
      data
    };
  };
}

/**
 * Polyfill of sorts for object.assign. To be removed once IE11 support is dropped
 * @param {object} output object containing all the key/value pairs of the source objects
 * @param {object} source one or more objects whose properties are to be merged into the output object
 * @returns {object} object with properties of all sources merged
 */
function assign( output = {}, source ) {
  const otherSources = Array.prototype.slice.call( arguments ).slice( 2 );
  const allSources = [ source ].concat( otherSources );
  const merged = Object.keys( output )
    .reduce( ( accum, k ) => {
      accum[k] = output[k];
      return accum;
    }, {} );
  const hasOwnProp = Object.prototype.hasOwnProperty;

  return allSources.reduce( ( accum, srcObj ) => {
    for ( const key in srcObj ) {
      if ( hasOwnProp.call( srcObj, key ) ) {
        const val = srcObj[key];
        accum[key] = val;
      }
    }

    return accum;
  }, merged );
}

/**
 * Helper function to determine if a value is an object
 * @param {object} maybeObject Value to be verified as an object
 * @returns {Boolean} whether or not the supplied value is an object
 */
function isObject( maybeObject ) {
  return maybeObject &&
    typeof maybeObject !== 'function' &&
    !( maybeObject instanceof Array ) &&
    typeof maybeObject === 'object';
}

/**
 * Function to convert an object into an array of arrays, when the first
 * element of each subarray corresponds to one of the object's keys, and
 * the second element corresponds to that key's value.
 *
 * @param {object} object The object to be converted into an array
 * @returns {Array} An array of arrays
 */
function entries( object ) {
  if ( !isObject( object ) ) {
    throw new Error( INVALID_OBJECT_ERROR );
  }

  const result = [];

  for ( const prop in object ) {
    if ( object.hasOwnProperty( prop ) ) {
      const value = object[prop];

      result.push( [ prop, value ] );
    }
  }

  return result;
}

export {
  actionCreator,
  assign,
  entries,
  UNDEFINED
};
