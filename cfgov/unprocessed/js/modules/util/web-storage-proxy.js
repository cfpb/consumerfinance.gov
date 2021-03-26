/* ==========================================================================
   Web Storage proxy utility.
   An interface for interacting with web storage
   (local storage and session storage).
   Note: values stored in local storage are not accessible from session storage
   and vice versa. They both work on different objects within the browser.
   If web storage is not available, values are dumped into an object literal
   to keep the fuctionality of the API, but will not be saved across sessions.
   ========================================================================= */

// Default storage type.
let _storage;

/**
 * Set an item value specified by the key in web storage.
 * @param {string} key The key for the value.
 * @param {string} value The value to store.
 * @param {Object} storage (Optional)
 *   Use non-persistent storage (sessionStorage)
 *   or persistent storage (localStorage).
 * @returns {string} The value set in web storage.
 */
function setItem( key, value, storage ) {
  storage = _getStorageType( storage );
  if ( storage.setItem ) {
    storage.setItem( key, value );
  } else {
    storage[key] = value;
  }

  return value;
}

/**
 * Get an item value specified by the key in web storage.
 * @param {string} key The key for the value.
 * @param {Object} storage (Optional)
 *   Use non-persistent storage (sessionStorage)
 *   or persistent storage (localStorage).
 * @returns {string} The value set in web storage.
 */
function getItem( key, storage ) {
  storage = _getStorageType( storage );

  return storage.getItem ? storage.getItem( key ) : storage[key];
}

/**
 * Remove an item specified by the key.
 * @param {string} key The key for the value.
 * @param {Object} storage (Optional)
 *   Use non-persistent storage (sessionStorage)
 *   or persistent storage (localStorage).
 * @returns {boolean} Returns true if the item existed and it was
 *   removed. Returns false if the item didn't exist to begin with.
 */
function removeItem( key, storage ) {
  storage = _getStorageType( storage );
  let returnVal = true;

  if ( !getItem( key, storage ) ) {
    returnVal = false;
  }

  if ( returnVal ) {
    if ( storage.removeItem ) {
      storage.removeItem( key );
    } else {
      delete storage[key];
    }
  }

  return returnVal;
}

/**
 * Set the default session type.
 * @param {Object} storage
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
 * @param {Object} storage
 *   Use non-persistent storage (sessionStorage)
 *   or persistent storage (localStorage).
 *   Default is sessionStorage.
 * @returns {Object} A local storage or session storage instance.
 */
function _getStorageType( storage ) {
  // Use default setting if none is provided.
  if ( storage === null || typeof storage !== 'object' ) {
    if ( typeof _storage === 'undefined' ) {
      try {
        storage = window.sessionStorage;
      } catch ( err ) {
        // SecurityError was thrown if cookies are off.
        storage = {};
      }
    } else {
      storage = _storage;
    }
  }

  return storage;
}

// Expose public methods.
export default {
  setItem,
  getItem,
  removeItem,
  setStorage
};
