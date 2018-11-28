/* ==========================================================================
   Expanded State Utils
   ========================================================================== */

let navTimeOut;

/**
 * @param {HTMLNode} elem Element to test.
 * @returns {boolean} True if element's aria-expanded value equals "true".
 */
function isThisExpanded( elem ) {
  return elem.getAttribute( 'aria-expanded' ) === 'true';
}

/**
 * Check if at least one element has a value of "true" set to an
 * aria-expanded attribute.
 *
 * @param {NodeList} elems List of elements to test.
 * @returns {boolean} True if at least one elements' aria-expanded value
 *   equals "true".
 */
function isOneExpanded( elems ) {
  let oneExpanded = false;

  for ( let i = 0, len = elems.length; i < len; i++ ) {
    if ( isThisExpanded( elems[i] ) ) {
      oneExpanded = true;
    }
  }

  return oneExpanded;
}

/**
 * Change the value of the element's aria-expanded attribute based on it's
 * current state if one is not passed. Allows for a delayed event for
 * animated elements.
 * @param {NodeList|Array|HTMLNode} elems
 *   List of elements or single element on which to set
 *   the aria-expanded attribute.
 * @param {string} state The value, if any, to set the aria-expanded
 *   attribute to. Options are "true", "false" or null.
 * @param {Function} cb The callback function to execute after a delay.
 * @param {integer} delay The length of time to delay the execution of
 *   the passed callback.
 */
function toggleExpandedState( elems, state, cb, delay ) {
  if ( elems.constructor !== NodeList &&
       elems.constructor !== Array ) {
    elems = [ elems ];
  }

  delay = delay || 300;
  state = state || !isOneExpanded( elems );

  for ( let i = 0, len = elems.length; i < len; i++ ) {
    elems[i].setAttribute( 'aria-expanded', state );
  }

  if ( cb ) {
    clearTimeout( navTimeOut );

    navTimeOut = setTimeout( function() {
      return cb();
    }, delay );
  }
}

export {
  isThisExpanded,
  isOneExpanded,
  toggleExpandedState
};
