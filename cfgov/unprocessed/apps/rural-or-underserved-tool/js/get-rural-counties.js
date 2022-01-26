require( 'es6-promise' ).polyfill();
import { fetch } from 'cross-fetch';


/* This cache currently isn't meaningfully used in any code path.
   If/when we implement better routing in this tool, it will be valuable. */
const cache = {};

/**
 * @param {string} year - A year.
 * @returns {Promise} An array of rural counties by fips.
 */
function getRuralCounties( year ) {
  if ( cache[year] ) return Promise.resolve( cache[year] );

  return fetch(
    'https://files.consumerfinance.gov/data/rural-or-underserved-tool/' +
    year + '.txt'
  ).then( v => v.text()
  ).then( v => {
    const val = v.split( '\n' );
    cache[year] = val;
    return val;
  } );
}


export default getRuralCounties;
