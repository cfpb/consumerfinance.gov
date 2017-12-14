/* ==========================================================================
   Atomic Helpers.
   Utilities for helping validate atomic design element architecture.
   In descending order of scope, atomic components are:
   - Page
   - Template
   - Organism
   - Molecule
   - Atom
   ========================================================================= */


const dataHook = require( './data-hook' );
const standardType = require( './standard-type' );

/**
 * @constant
 * @type {string}
 * @description
 * Flag that gets set on an atomic component after its .init()
 * method has been called. This is used so that an atomic
 * component won't get initialized a second time after it
 * has already been initialized.
 */
const INIT_FLAG = standardType.STATE_PREFIX + 'atomic_init';

/**
 * Check that a particular element passed into the constructor of
 * an atomic component exists and that the correct atomic class
 * is present on the element.
 * @param {HTMLNode} element
 *   The DOM element within which to search for the atomic element class.
 * @param {string} baseClass - The CSS class name for the atomic element.
 * @returns {HTMLNode} The DOM element for the atomic element.
 * @throws {Error} If DOM element passed into the atomic element is not valid.
 */
function checkDom( element, baseClass ) {
  _verifyElementExists( element, baseClass );
  const dom = _verifyClassExists( element, baseClass );

  return dom;
}

/**
 * @param {HTMLNode} element
 *   The DOM element within which to search for the atomic element class.
 * @param {string} baseClass - The CSS class name for the atomic element.
 * @returns {HTMLNode} The DOM element for the atomic element.
 * @throws {Error} If DOM element passed into the atomic element is not valid.
 */
function _verifyElementExists( element, baseClass ) {
  if ( !element || !element.classList ) {
    const msg = element + ' is not valid. ' +
              'Check that element is a DOM node with class "' +
              baseClass + '"';
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
  const dom = element.classList.contains( baseClass ) ?
    element : element.querySelector( '.' + baseClass );
  if ( !dom ) {
    const msg = baseClass + ' not found on or in passed DOM node.';
    throw new Error( msg );
  }

  return dom;
}

/**
 * Set a flag on an atomic component when it is initialized.
 * Use the returned boolean to handle cases where an atomic component
 * is initializing when it has already been initialized elsewhere.
 * @param {HTMLNode} element - The DOM element for the atomic component.
 * @param {null} destroy - Pass in true to .
 * @returns {boolean} True if the init data-js-* hook attribute was set,
 *   false otherwise.
 */
function setInitFlag( element ) {
  if ( dataHook.contains( element, INIT_FLAG ) ) {
    return false;
  }

  dataHook.add( element, INIT_FLAG );

  return true;
}

/**
 * Remove the initialization flag on an atomic component.
 * This might be used if the DOM of an atomic element is cloned.
 * @param {HTMLNode} element - The DOM element for the atomic component.
 * @returns {boolean} True if the init data-js-* hook attribute was destroyed,
 *   otherwise false if it didn't exist.
 */
function destroyInitFlag( element ) {
  if ( !dataHook.contains( element, INIT_FLAG ) ) {
    return false;
  }

  dataHook.remove( element, INIT_FLAG );

  return true;
}

/**
 * @param {string} selector - Selector to search for in the document.
 * @param {Function} Constructor - A constructor function.
 * @returns {Array} List of instances that were instantiated.
 */
function instantiateAll( selector, Constructor ) {
  const all = document.querySelectorAll( selector );
  let inst;
  const insts = [];
  for ( let i = 0, len = all.length; i < len; i++ ) {
    inst = new Constructor( all[i] );
    inst.init();
    insts.push( inst );
  }
  return insts;
}

// Expose public methods.
module.exports = {
  checkDom:        checkDom,
  destroyInitFlag: destroyInitFlag,
  instantiateAll:  instantiateAll,
  setInitFlag:     setInitFlag
};
