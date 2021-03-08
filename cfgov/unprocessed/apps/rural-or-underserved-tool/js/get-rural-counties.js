require( 'es6-promise' ).polyfill();
import { fetch } from 'cross-fetch';

/**
 * @param {string} year - A year.
 * @returns {Object} Result of the call to a JSON file.
 */
function getRuralCounties( year ) {
  return fetch(
    'https://files.consumerfinance.gov/rural-or-underserved-tool/data/' +
    year + '.json'
  ).then( v => v.json() );
}

export default getRuralCounties;
