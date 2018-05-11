import config from '../../config.json';

const axios = require( 'axios' );
const CancelToken = axios.CancelToken;

let _cancelToken;

/**
 * @returns {CancelToken} A cancel token used in getData to provide a means to
 *   cancel the request to the API.
 *   This is used by the unit tests to check the values sent to the API.
 */
function getLastCancelToken() {
  return _cancelToken;
}

/**
 * Get data from the API.
 * @param {Object} fieldToFetch - Hash of fields to add to the query.
 * @returns {Promise} A promise for the XMLHttpRequest request.
 */
function getData( fieldToFetch ) {
  const today = new Date();
  const decache = String( today.getDate() ) + today.getMonth();

  let cancelFunc;
  _cancelToken = new CancelToken( function executor( newCancelFunc ) {
    // An executor function receives a cancel function as a parameter.
    cancelFunc = newCancelFunc;
  } );

  const params = Object.assign(
    { decache: decache, cancelToken: _cancelToken }, fieldToFetch
  );

  return {
    promise: axios.get(
      config.rateCheckerAPI,
      { params: params }
    ),
    cancel: cancelFunc
  };
}

/**
 * Get a list of counties from the API for the selected state.
 * @param {string} forState - The state to get counties for.
 * @returns {Promise} A promise for the XMLHttpRequest request.
 */
function getCounties( forState ) {
  return {
    promise: axios.get(
      config.countyAPI,
      { params: { state: forState }}
    )
  };
}

module.exports = {
  getLastCancelToken,
  getData,
  getCounties
};
