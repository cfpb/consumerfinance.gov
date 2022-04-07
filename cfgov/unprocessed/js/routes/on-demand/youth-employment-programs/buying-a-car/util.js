/**
 * Converts values to arrays. Array-like objects (such as NodeList) will be filled with their values,
 * all other values return an empty array
 * @param {*} arrayLike The value to be converted to an array
 * @returns {Array} The supplied value wrapped in an array if it is an array-like object,
 * an empty array otherwise
 */
function toArray( arrayLike ) {
  return Array.prototype.slice.call( arrayLike );
}

export {
  toArray
};
