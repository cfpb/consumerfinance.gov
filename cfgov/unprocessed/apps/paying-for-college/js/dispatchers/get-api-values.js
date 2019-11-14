import { promiseRequest } from '../util/promise-request';

const schoolSearch = function( searchTerm ) {
  const url = '/paying-for-college2/understanding-your-financial-aid-offer' +
    '/api/search-schools.json?q=' + searchTerm;
  const xhr = new XMLHttpRequest();
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


export {
  schoolSearch
};
