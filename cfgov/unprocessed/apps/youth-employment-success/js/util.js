let UNDEFINED;

const REDUCER_RETURN_ERROR = 'Reducer must return a state object';
const INVALID_ARG_ERROR = 'The "reducers" argument must be an object, where each value is a reducer function';
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
 *
 * @param {object} state Composed of key / value pairs where the key is the name of
 *  a slice of app state, and the value is the values for that slice of state
 * @param {string} key name of the state slice
 * @returns {function|undefined} Return the reducer function or undefined
 */
function checkForPreviousState( state = {}, key ) {
  if ( state[key] ) {
    return state[key];
  }

  return UNDEFINED;
}

/**
 * Throw an error if the reducer processing the current action doesn't return
 * a value
 * @param {object} nextState The state object just returned by a reducer
 */
function assertNextState( nextState ) {
  if ( typeof nextState === 'undefined' ) {
    throw new Error( REDUCER_RETURN_ERROR );
  }
}

const processStateFromReducers = reducers => (
  state = UNDEFINED,
  action = { type: null }
) => {
  const reducersKeys = Object.keys( reducers );
  const finalState = {};
  let hasChanged = false;

  for ( let i = 0; i < reducersKeys.length; i++ ) {
    const key = reducersKeys[i];
    const reducer = reducers[key];

    /**
     * If we didnt already get a composite state object, e.g. if this is
     * the first time the reducers are running, default to undefined
     * and force the reducer to use it's default state.
     */
    const previousState = checkForPreviousState( state, key );
    const argumentsToApply = [ previousState, action ];
    const nextState = reducer.apply( reducer, argumentsToApply );

    assertNextState( nextState );

    finalState[key] = nextState;
    hasChanged = hasChanged || nextState !== previousState;
  }

  return hasChanged ? finalState : state;
};

const combineReducers = reducers => {
  if ( !isObject( reducers ) ) {
    throw new TypeError( INVALID_ARG_ERROR );
  }

  const list = entries( reducers );

  const combinedReducers = list.reduce( ( memo, [ name, maybeFunc ] ) => {
    if ( typeof maybeFunc === 'function' ) {
      memo[name] = maybeFunc;
    }

    return memo;
  }, {} );

  return processStateFromReducers( combinedReducers );
};

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

/**
 * Converts values to arrays. Array-like objects (such as NodeList) will be filled with their values,
 * all other values return an empty array
 * @param {*} arrayLike The value to be converted to an array
 * @returns {Array} The supplied value wrapped in an array if it is an array-like object,
 * an empty array otherwise
 */
function toArray( arrayLike ) {
  return Array.prototype.slice.call( arrayLike );
}

/**
 * Test if value is a number
 * @param {*} maybeNum A potentially numberical value
 * @returns {Boolean} If value is a number or not
 */
function isNumber( maybeNum ) {
  // NaN is never equal to itself, and is thus the only real way pre es6 to check for its existence
  const num = Number( maybeNum );
  // eslint-disable-next-line no-self-compare
  return typeof num === 'number' && num === num;
}

export {
  actionCreator,
  assign,
  combineReducers,
  entries,
  isNumber,
  toArray,
  UNDEFINED
};
