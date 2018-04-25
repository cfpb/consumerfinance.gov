import config from '../../config.json';

/**
 * Make an XHR request.
 * @param {string} method - 'GET' or 'POST'.
 * @param {string} url - The URL to request.
 * @param {Object} data - Data to pass to the request.
 * @return {Promise} A promise for the XMLHttpRequest request.
 */
function _makeRequest( method, url, data ) {

  if ( method === 'GET' ) {
    let queryString = '?';
      for ( let item in data ) {
        queryString += `${ item }=${ data[item] }&`;
      }
    url += queryString;
    data = null;
  }

  const promise = new Promise( (resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open( method, url );
    xhr.onload = evt => {
      if ( xhr.status >= 200 && xhr.status < 300 ) {
        return resolve( xhr.response );
      }

      reject( {
        status:     xhr.status,
        statusText: xhr.statusText
      } );
    };
    xhr.onerror = () => {
      reject( {
        status:     xhr.status,
        statusText: xhr.statusText
      } );
    };
    xhr.send( data );
  } );

  return promise;
}

/**
 * Get data from the API.
 * @returns {Promise} A promise for the XMLHttpRequest request.
 */
function getData( fieldToFetch ) {
  const today = new Date();
  const decache = String( today.getDate() ) + today.getMonth();

  const promise = _makeRequest(
    'GET',
    config.rateCheckerAPI,
    Object.assign( { decache: decache }, fieldToFetch )
  );

  return promise;
}

/**
 * Get a list of counties from the API for the selected state.
 * @param {string} forState - The state to get counties for.
 * @returns {Promise} A promise for the XMLHttpRequest request.
 */
function getCounties( forState ) {
  return _makeRequest( 'GET', config.countyAPI, { state: forState } );
}

module.exports = {
  getData,
  getCounties
};
