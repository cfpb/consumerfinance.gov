let UNDEFINED;

/* checkHudData() just makes sure your data has the correct structure
before you start requesting properties that don't exist in _updateMap()
*/

/**
 * Make sure your data has the correct structure
 * before you start requesting properties that don't exist in updateMap()
 * @param {object} data - The data object to check for a valid structure.
 * @returns {boolean} True if the data object is valid, false otherwise.
 */
function checkHudData(data) {
  if (data === null || data === 0 || data === UNDEFINED) {
    return false;
  } else if (
    {}.hasOwnProperty.call(data, 'error') ||
    !{}.hasOwnProperty.call(data, 'counseling_agencies') ||
    !{}.hasOwnProperty.call(data, 'zip')
  ) {
    return false;
  }

  return true;
}

export { checkHudData };
