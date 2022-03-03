/**
 * Polyfill of sorts for object.assign. To be removed once IE11 support is dropped
 * @param {object} output object containing all the key/value pairs of the source objects
 * @param {object} source one or more objects whose properties are to be merged into the output object
 * @returns {object} object with properties of all sources merged
 */
function assign(output = {}, source) {
  const otherSources = Array.prototype.slice.call(arguments).slice(2);
  const allSources = [source].concat(otherSources);
  const merged = Object.keys(output)
    .reduce((accum, k) => {
      accum[k] = output[k];
      return accum;
    }, {});
  const hasOwnProp = Object.prototype.hasOwnProperty;

  return allSources.reduce((accum, srcObj) => {
    for (const key in srcObj) {
      if (hasOwnProp.call(srcObj, key)) {
        const val = srcObj[key];
        accum[key] = val;
      }
    }

    return accum;
  }, merged);
}

/**
 * Converts values to arrays. Array-like objects (such as NodeList) will be filled with their values,
 * all other values return an empty array
 * @param {*} arrayLike The value to be converted to an array
 * @returns {Array} The supplied value wrapped in an array if it is an array-like object,
 * an empty array otherwise
 */
function toArray(arrayLike) {
  return Array.prototype.slice.call(arrayLike);
}

export {
  assign,
  toArray
};
