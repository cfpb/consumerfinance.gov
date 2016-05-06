/* ==========================================================================
   Atomic Helpers.
   Utilities for helping validate atomic design element architecture.
   ========================================================================= */

'use strict';

var dataHook = require( './data-hook' );

// TODO: Update baseClass to baseSel to handle CSS selector instead of a class.
/**
 * @param {HTMLNode} element
 *   The DOM element within which to search for the atomic element class.
 * @param {string} baseClass The CSS class name for the atomic element.
 * @param {string} atomicName
 *   The name of the atomic element in CapitalizedCamelCase.
 * @returns {HTMLNode} The DOM element for the atomic element.
 * @throws {Error} If DOM element passed into the atomic element is not valid.
 */
function checkDom( element, baseClass, atomicName ) {
  _verifyElementExists( element, atomicName );
  var dom = _verifyClassExists( element, baseClass );

  return dom;
}

/**
 * @param {HTMLNode} element
 *   The DOM element within which to search for the atomic element class.
 * @param {string} atomicName
 *   The name of the atomic element in CapitalizedCamelCase.
 * @returns {HTMLNode} The DOM element for the atomic element.
 * @throws {Error} If DOM element passed into the atomic element is not valid.
 */
function _verifyElementExists( element, atomicName ) {
  if ( !element || !element.classList ) {
    var msg = element + ' passed to ' + atomicName + '.js is not valid. ' +
              'Check that element is a valid DOM node';
    throw new Error( msg );
  }

  return element;
}

/**
 * @param {HTMLNode} element
 *   The DOM element within which to search for the atomic element class.
 * @param {string} baseClass The CSS class name for the atomic element.
 * @returns {HTMLNode} The DOM element for the atomic element.
 * @throws {Error} If baseClass was not found on the element.
 */
function _verifyClassExists( element, baseClass ) {
  var dom = element.classList.contains( baseClass ) ?
            element : element.querySelector( '.' + baseClass );
  if ( !dom ) {
    var msg = baseClass + ' not found on or in passed DOM node.';
    throw new Error( msg );
  }

  return dom;
}

/**
 * Set a flag on an atomic component when it is initialized.
 * Use the returned boolean to handle cases where an atomic component
 * is initializing when it has already been initialized elsewhere.
 * @param {HTMLNode} element
 *   The DOM element within which to search for the atomic element class.
 * @returns {boolean} True if the init data-js-* hook attribute was set,
 *   false otherwise.
 */
function setInitFlag( element ) {
  if ( dataHook.contains( element, 'init' ) ) {
    return false;
  }

  dataHook.add( element, 'init' );

  return true;
}

/**
 * @param {string} selector - Selector to search for in the document.
 * @param {Function} Constructor - A constructor function.
 * @returns {Array} List of instances that were instantiated.
 */
function instantiateAll( selector, Constructor ) {
  var all = document.querySelectorAll( selector );
  var inst;
  var insts = [];
  for ( var i = 0, len = all.length; i < len; i++ ) {
    inst = new Constructor( all[i] );
    inst.init();
    insts.push( inst );
  }
  return insts;
}

// Expose public methods.
module.exports = {
  checkDom: checkDom,
  instantiateAll: instantiateAll,
  setInitFlag: setInitFlag
};
