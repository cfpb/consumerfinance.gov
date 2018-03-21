/**
 * Mock an object store.
 * @returns {Object} A new object store with general access methods.
 */
function storageMock() {
  const storage = {};
  return {
    setItem: function( key, value ) {
      storage[key] = value || '';
    },
    getItem: function( key ) {
      return storage[key];
    },
    removeItem: function( key ) {
      delete storage[key];
    },
    get length() {
      return Object.keys( storage ).length;
    },
    key: function( i ) {
      const keys = Object.keys( storage );
      return keys[i] || null;
    }
  };
}

module.exports = storageMock;
