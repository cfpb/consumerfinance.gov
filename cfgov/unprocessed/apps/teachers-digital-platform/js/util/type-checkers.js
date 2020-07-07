/* ==========================================================================
   Javascript Type Checkers
   Various utility functions to check Javascript types and primitives.
   Copied from:
   https://github.com/angular/angular.js/blob/master/src/Angular.js.
   Copyright (c) 2010-2015 Google, Inc. https://angularjs.org
   ========================================================================== */


const _toString = Object.prototype.toString;

/**
 * @name isUndefined
 * @kind function
 *
 * @description
 * Determines if a reference is undefined.
 *
 * @param {*} value Reference to check.
 * @returns {boolean} True if `value` is undefined.
 */
function isUndefined( value ) {
  return typeof value === 'undefined';
}


/**
 * @name isDefined
 * @kind function
 *
 * @description
 * Determines if a reference is defined.
 *
 * @param {*} value Reference to check.
 * @returns {boolean} True if `value` is defined.
 */
function isDefined( value ) {
  return typeof value !== 'undefined';
}


/**
 * @name isObject
 * @kind function
 *
 * @description
 * Determines if a reference is an `Object`.
 * Unlike `typeof` in JavaScript, `null`s are not
 * considered to be objects. Note that JavaScript arrays are objects.
 *
 * @param {*} value Reference to check.
 * @returns {boolean} True if `value` is an `Object` but not `null`.
 */
function isObject( value ) {
  // https://jsperf.com/isobject4
  return value !== null && typeof value === 'object';
}


/**
 * @name isString
 * @kind function
 *
 * @description
 * Determines if a reference is a `String`.
 *
 * @param {*} value Reference to check.
 * @returns {boolean} True if `value` is a `String`.
 */
function isString( value ) {
  return _toString.call( value ) === '[object String]';
}


/**
 * @name isNumber
 * @kind function
 *
 * @description
 * Determines if a reference is a `Number`.
 *
 * This includes the "special" numbers `NaN`, `+Infinity` and `-Infinity`.
 *
 * If you wish to exclude these then you can use the native
 * [`isFinite'](https://developer.mozilla.org/en-US/docs/Web/JavaScript/
 *                      Reference/Global_Objects/isFinite)
 * method.
 *
 * @param {*} value Reference to check.
 * @returns {boolean} True if `value` is a `Number`.
 */
function isNumber( value ) {
  return _toString.call( value ) === '[object Number]';
}


/**
 * @name isDate
 * @kind function
 *
 * @description
 * Determines if a value is a date.
 *
 * @param {*} value Reference to check.
 * @returns {boolean} True if `value` is a `Date`.
 */
function isDate( value ) {
  return _toString.call( value ) === '[object Date]';
}


/**
 * @name isArray
 * @kind function
 *
 * @description
 * Determines if a reference is an `Array`.
 *
 * @param {*} value Reference to check.
 * @returns {boolean} True if `value` is an `Array`.
 */
const isArray = Array.isArray || function isArray( value ) {
  return _toString.call( value ) === '[object Array]';
};


/**
 * @name isFunction
 * @kind function
 *
 * @description
 * Determines if a reference is a `Function`.
 *
 * @param {*} value Reference to check.
 * @returns {boolean} True if `value` is a `Function`.
 */
function isFunction( value ) {
  return _toString.call( value ) === '[object Function]';
}

/**
 * @name isEmpty
 * @kind function
 *
 * @description
 * Determines if a reference is empty.
 *
 * @param {*} value Reference to check.
 * @returns {boolean} True if `value` is empty.
 */
function isEmpty( value ) {
  return isUndefined( value ) ||
         value === null ||
         isString( value ) &&
         value.length <= 0 ||
         ( /^\s*$/ ).test( value );
}


// Expose public methods.
module.exports = {
  isUndefined: isUndefined,
  isDefined:   isDefined,
  isObject:    isObject,
  isString:    isString,
  isNumber:    isNumber,
  isDate:      isDate,
  isArray:     isArray,
  isFunction:  isFunction,
  isEmpty:     isEmpty
};
