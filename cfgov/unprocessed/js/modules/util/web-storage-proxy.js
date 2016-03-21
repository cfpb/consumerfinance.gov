/* ==========================================================================
   Web Storage proxy utility.

   An interface for interacting with web storage
   (local storage and session storage).
   Note: values stored in local storage are not accessible from session storage
   and vice versa. They both work on different objects within the browser.
   ========================================================================= */

'use strict';

// Default storage type.
var _storage = window.sessionStorage;

/**
 * Set an item value specified by the key in web storage.
 * @param {string} key The key for the value.
 * @param {string} value The value to store.
 * @param {object} storage (Optional)
 *   Use non-persistent storage (sessionStorage)
 *   or persistent storage (localStorage).
 * @returns {string} The value set in web storage.
 */
function setItem( key, value, storage ) {
  storage = _getStorageType( storage );
  storage.setItem( key, value );

  return value;
}

/**
 * Get an item value specified by the key in web storage.
 * @param {string} key The key for the value.
 * @param {object} storage (Optional)
 *   Use non-persistent storage (sessionStorage)
 *   or persistent storage (localStorage).
 * @returns {string} The value set in web storage.
 */
function getItem( key, storage ) {
  storage = _getStorageType( storage );

  return storage.getItem( key );
}

/**
 * Remove an item specified by the key.
 * @param {string} key The key for the value.
 * @param {object} storage (Optional)
 *   Use non-persistent storage (sessionStorage)
 *   or persistent storage (localStorage).
 * @returns {boolean} Returns true if the item existed and it was
 *   removed. Returns false if the item didn't exist to begin with.
 */
function removeItem( key, storage ) {
  storage = _getStorageType( storage );
  var returnVal = true;

  if ( !storage.getItem( key ) ) {
    returnVal = false;
  }

  if ( returnVal ) {
    storage.removeItem( key );
  }

  return returnVal;
}

/**
 * Set the default session type.
 * @param {object} storage
 *   Use non-persistent storage (sessionStorage)
 *   or persistent storage (localStorage).
 * @throws {Error} If parameter isn't a object.
 */
function setStorage( storage ) {
  if ( typeof storage !== 'object' ) {
    throw new Error( 'Setting must be an object.' );
  }

  _storage = storage;
}

/**
 * Internal function for whether to use local or session storage.
 * @param {object} storage
 *   Use non-persistent storage (sessionStorage)
 *   or persistent storage (localStorage).
 * @returns {object} A local storage or session storage instance.
 */
function _getStorageType( storage ) {
  // Use default setting if none is provided.
  if ( typeof storage !== 'object' ) {
    if ( typeof _storage === 'undefined' ) {
      storage = window.sessionStorage;
    } else {
      storage = _storage;
    }
  }

  return storage;
}

// Expose public methods.
module.exports = {
  setItem:    setItem,
  getItem:    getItem,
  removeItem: removeItem,
  setStorage: setStorage
};
