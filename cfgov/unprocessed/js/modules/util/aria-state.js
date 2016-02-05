/* ==========================================================================
   ARIA State

   Code conventions copied from the following with major modifications:

   - https://github.com/IBM-Watson/a11y.js
     Copyright (c) 2014 IBM
   ========================================================================== */

'use strict';

var ariaStatesConfig = require( '../../config/aria-states-config' );

// Properties
var ariaState;

// Constants
var STATE_PREFIX = 'is';
var ARIA_STATE_PREFIX = 'aria-';


// Private Methods

/**
 * Defines ARIA state propery on an object.
 *
 * @param {string} state - ARIA state.
 * @param {HTMLElement} element - Element in which to apply
                                  the ARIA state attribute.
 * @param {object} object - Object in which to apply the ARIA state.
 * @returns {object}.
 */
function _defineProperty( state, element, object ) {
  var _value = object[state] || false;
  var _state = state;
  var _element = element;

  Object.defineProperty( object, state, {
    enumerable:   true,
    configurable: true,

    get: function() {
      return _value;
    },

    set: function( value ) {
      _value = value;
      ariaState.set( _state, _element, _value );
    }
  } );

  ariaState.set( _state, _element, _value );

  return object;
}

/**
 * Validates ARIA state exists using config file.
 *
 * @param {string} state - ARIA state.
 * @returns {Boolean} - Value indicating if ARIA state is valid.
 */
function _validateState( state ) {
  return Boolean( ariaStatesConfig[ARIA_STATE_PREFIX + state] );
}


// Public Methods

ariaState = {

  /**
   * Creates ARIA state on an object.
   *
   * @param {string} state - ARIA state.
   * @param {HTMLElement} element - Element in which to apply
                                    the ARIA state attribute.
   * @returns {object} - Object with defined ARIA state.
   */
  create: function create( state, element ) {
    if ( _validateState( state ) === false ||
         element instanceof HTMLElement === false ) {
      throw new Error( 'Invalid Arguments' );
    }

    return this.define( state, element, {} );
  },

  /**
   * Defines ARIA state string using prefix. Calls internal
   * function to define ARIA state property on an object.
   *
   * @param {string} state - ARIA state.
   * @param {HTMLElement} element - Element in which to apply
                                    the ARIA state attribute.
   * @param {object} object - Value of the ARIA state attribute.
   * @returns {object} - Object with define ARIA state.
   */
  define: function define( state, element, object ) {
    if ( _validateState( state ) ) {
      state = STATE_PREFIX + state.charAt( 0 ).toUpperCase() +
              state.substring( 1 );
      _defineProperty( state, element, object );
    }

    return object;
  },

  /**
   * Gets ARIA state attribute value from dom element.
   *
   * @param {string} state - ARIA state.
   * @param {HTMLElement} element - Element in which to apply
                                    the ARIA state attribute.
   * @returns {value} - ARIA state attribute value.
   */
  get: function get( state, element ) {
    return element.getAttribute( ariaStatesConfig[ARIA_STATE_PREFIX + state] );
  },

  /**
   * Sets ARIA state attribute on a dom elment.
   *
   * @param {string} state - ARIA state.
   * @param {HTMLElement} element - Element in which to apply
                                    the ARIA state attribute.
   * @param {string} value - Value of the ARIA state attribute.
   * @returns {element} - dom element.
   */
  set: function set( state, element, value ) {
    state = state.substr( 0, 2 ) === STATE_PREFIX && state.substr( 2 ) || state;
    state = state.toLowerCase();
    if ( _validateState( state ) ) {
      state = ARIA_STATE_PREFIX + state;
      element.setAttribute( state, value );
    }

    return element;
  }

};

module.exports = ariaState;
