import { promiseRequest } from '../util/promise-request';

/**
 * schoolSearch - search for schools based on searchTerm
 * @param {String} searchTerm - Term to be searched for
 * @returns {Object} Promise
 */
const schoolSearch = function( searchTerm ) {
  const url = '/paying-for-college2/understanding-your-financial-aid-offer' +
    '/api/search-schools.json?q=' + searchTerm;
  return new Promise( function( resolve, reject ) {
    promiseRequest( 'GET', url )
      .then( function( resp ) {
        resolve( resp );
      } )
      .catch( function( error ) {
        reject( new Error( error ) );
        console.log( 'An error occurred!', error );
      } );
  } );
};

/**
 * getConstants - retrieve constants from our API
 * @returns {Object} Promise
 */
const getConstants = function() {
  const url = '/paying-for-college2/understanding-your-financial-aid-offer' +
    '/api/constants/';
  return new Promise( function( resolve, reject ) {
    promiseRequest( 'GET', url )
      .then( function( resp ) {
        resolve( resp );
      } )
      .catch( function( error ) {
        reject( new Error( error ) );
        // console.log( 'An error occurred!', error );
      } );
  } );
};

/**
 * getExpenses - retrieve expense data from our API
 * @returns {Object} Promise
 */
const getExpenses = function() {
  const url = '/paying-for-college2/understanding-your-financial-aid-offer' +
    '/api/expenses/';
  return new Promise( function( resolve, reject ) {
    promiseRequest( 'GET', url )
      .then( function( resp ) {
        resolve( resp );
      } )
      .catch( function( error ) {
        reject( new Error( error ) );
        // console.log( 'An error occurred!', error );
      } );
  } );
};

/**
 * getSchoolData - retrieve school data from our API
 * @param { String } iped - The school's identification number
 * @returns {Object} Promise
 */
const getSchoolData = function( iped ) {
  const url = '/paying-for-college2/understanding-your-financial-aid-offer' +
    '/api/school/' + iped;

  const xhr = new XMLHttpRequest();

  return new Promise( function( resolve, reject ) {
    promiseRequest( 'GET', url )
      .then( function( resp ) {
        resolve( resp );
      } )
      .catch( function( error ) {
        reject( new Error( error ) );
        // console.log( 'An error occurred!', error );
      } );
  } );
};

export {
  getConstants,
  getExpenses,
  getSchoolData,
  schoolSearch
};
