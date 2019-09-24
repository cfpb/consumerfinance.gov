require( 'es6-promise' ).polyfill();
import { get } from 'axios';

/**
 * @param {string} year - A year.
 * @returns {Object} Result of the call to a JSON file.
 */
function getRuralCounties( year ) {
  return get(
    'https://files.consumerfinance.gov/rural-or-underserved-tool/data/' +
    year + '.json'
  );
}

export default getRuralCounties;
