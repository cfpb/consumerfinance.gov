import { promiseRequest } from '../util/promise-request';

/**
 * getApi - Make an API request to the endpoint specified with parameters specified
 * @param {string} url - URL of API endpoint
 * @param {string} parameter - Additional parameter, if applicable
 * @returns {Object} Promise
 */
function getApi( url ) {
  return new Promise( function( resolve, reject ) {
    promiseRequest( 'GET', url )
      .then( function( resp ) {
        resolve( resp );
      } )
      .catch( function( error ) {
        console.log( 'An error occurred accessing ' + url, error );
        reject( new Error( error ) );
      } );
  } );
}

/**
 * schoolSearch - search for schools based on searchTerm
 * @param {String} searchTerm - Term to be searched for
 * @returns {Object} Promise
 */
function schoolSearch( searchTerm ) {
  searchTerm = searchTerm.trim();
  if ( searchTerm.length > 2 ) {
    const url = '/paying-for-college2/understanding-your-financial-aid-offer' +
      '/api/search-schools.json?q=' + searchTerm;
    return getApi( url );
  }
  return Promise.reject( new Error( 'Failure - search term too short' ) );
}

/**
 * getConstants - retrieve constants from our API
 * @returns {Object} Promise
 */
function getConstants() {
  const url = '/paying-for-college2/understanding-your-financial-aid-offer' +
    '/api/constants/';
  return getApi( url );
}

/**
 * getExpenses - retrieve expense data from our API
 * @returns {Object} Promise
 */
function getExpenses() {
  const url = '/paying-for-college2/understanding-your-financial-aid-offer' +
    '/api/expenses/';
  return getApi( url );
}

/**
 * getSchoolData - retrieve school data from our API
 * @param { String } iped - The school's identification number
 * @returns {Object} Promise
 */
function getSchoolData( iped ) {
  const url = '/paying-for-college2/understanding-your-financial-aid-offer' +
    '/api/school/' + iped;

  return getApi( url );
}

export {
  getConstants,
  getExpenses,
  getSchoolData,
  schoolSearch
};
