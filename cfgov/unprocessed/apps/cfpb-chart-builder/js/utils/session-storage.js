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
 * @param {string} key - The key for the value.
 * @param {string} value - The value to store.
 * @param {object} storage - (Optional)
 *   Use non-persistent storage (sessionStorage)
 *   or persistent storage (localStorage).
 * @returns {string} The value set in web storage.
 */
function setItem(key, value, storage) {
  value = JSON.stringify(value);
  storage = _getStorageType(storage);
  if (storage.setItem) {
    storage.setItem(key, value);
  } else {
    storage[key] = value;
  }

  return value;
}

/**
 * Get an item value specified by the key in web storage.
 * @param {string} key - The key for the value.
 * @param {object} storage - (Optional)
 *   Use non-persistent storage (sessionStorage)
 *   or persistent storage (localStorage).
 * @returns {string} The value set in web storage.
 */
function getItem(key, storage) {
  storage = _getStorageType(storage);
  if (storage.getItem) {
    return JSON.parse(storage.getItem(key));
  }
  return JSON.parse(storage[key]);
}

/**
 * Remove an item specified by the key.
 * @param {string} key - The key for the value.
 * @param {object} storage - (Optional)
 *   Use non-persistent storage (sessionStorage)
 *   or persistent storage (localStorage).
 * @returns {boolean} Returns true if the item existed and it was
 *   removed. Returns false if the item didn't exist to begin with.
 */
function removeItem(key, storage) {
  storage = _getStorageType(storage);
  let returnVal = true;

  if (!getItem(key, storage)) {
    returnVal = false;
  }

  if (returnVal) {
    if (storage.removeItem) {
      storage.removeItem(key);
    } else {
      delete storage[key];
    }
  }

  return returnVal;
}

/**
 * Internal function for whether to use local or session storage.
 * @param {object} storage - Use non-persistent storage (sessionStorage)
 *   or persistent storage (localStorage).
 * @returns {object} A local storage or session storage instance.
 */
function _getStorageType(storage) {
  // Use default setting if none is provided.
  if (typeof storage !== 'object') {
    if (typeof _storage === 'undefined') {
      try {
        storage = window.sessionStorage;
      } catch {
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
};
