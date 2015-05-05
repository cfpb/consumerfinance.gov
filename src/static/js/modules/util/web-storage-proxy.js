/* ==========================================================================
   Web Storage proxy utility.

   An interface for interacting with web storage
   (local storage and session storage).
   A final parameter of true on all methods specifies to use session storage
   (non-persistant storage). A final parameter of false on all methods
   specifies to use local storage (persistent storage).
   E.g. webStorageProxy.setItem("name", "Anselm", true)
   for session storage or webStorageProxy.getItem("name")
   for local storage (note omitted 'true' value).
   Note: values stored in local storage are not accessible from session storage
   and vice versa. They both work on different objects within the browser.
   ========================================================================== */

'use strict';

// Default session type.
// true = sessionStorage (non-persistent).
// false = localStorage (persistent).
var _sessionOnly = false;

// Set an item value specified by the key in web storage.
// @param key {String} The key for the value.
// @param value {String} The value to store.
// @param sessionOnly {Boolean} (Optional)
//   Use non-persistent storage (true) or persistent storage (false).
// @return {String} The value set in web storage.
function setItem( key, value, sessionOnly ) {
  var storage = _sessionOrLocal( sessionOnly );
  storage.setItem( key, value );
  return value;
}

// Get an item value specified by the key in web storage.
// @param key {String} The key for the value.
// @param sessionOnly {Boolean} (Optional)
//   Use non-persistent storage (true) or persistent storage (false).
// @return {String} The value set in web storage.
function getItem( key, sessionOnly ) {
  var storage = _sessionOrLocal( sessionOnly );
  return storage.getItem( key );
}

// Remove an item specified by the key.
// @param key {String} The key for the value.
// @param sessionOnly {Boolean} (Optional)
//   Use non-persistent storage (true) or persistent storage (false).
// @return {Boolean} Returns true if the item existed and it was
//   removed. Returns false if the item didn't exist to begin with.
function removeItem( key, sessionOnly ) {
  var storage = _sessionOrLocal( sessionOnly );
  var returnVal = true;
  if ( !storage.getItem( key ) ) returnVal = false;
  if ( returnVal ) storage.removeItem( key );

  return returnVal;
}

// Internal function for setting default session type.
// Throws an error if parameter isn't a boolean.
// @param sessionOnly {Boolean}
//   Use non-persistent storage (true) or persistent storage (false).
function setSessionType( sessionOnly ) {
  if ( typeof sessionOnly !== 'boolean' ) {
    throw new Error( 'Setting requires a boolean value.' );
  }
  _sessionOnly = sessionOnly;
}

// Internal function for whether to use local or session storage.
// @param sessionOnly {Boolean}
//   Use non-persistent storage (true) or persistent storage (false).
// @return {Object} A local storage or session storage instance.
function _sessionOrLocal( sessionOnly ) {
  // Use default setting if none is provided.
  if ( typeof sessionOnly === 'undefined' ) sessionOnly = _sessionOnly;
  var storage;
  if ( sessionOnly ) storage = sessionStorage;
  else storage = localStorage;
  return storage;
}

// Expose public methods.
module.exports = {
    setItem:        setItem,
    getItem:        getItem,
    removeItem:     removeItem,
    setSessionType: setSessionType
};
