require( 'es6-promise' ).polyfill();
const jsonP = require( 'jsonp-p' ).default;
import DT from './dom-tools';
import count from './count';

/**
 * Call the census.gov API and display an error if warranted.
 * @param {string} address - An address.
 * @param {Object} rural - Rural data via json file.
 * @param {*} cb - Callback to call (unused).
 */
function callCensus( address, rural, cb ) {
  let url = 'https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?';
  url += 'address=' + address;
  url += '&benchmark=4';
  url += '&format=jsonp';

  jsonP( url ).promise
    .then( function( data ) {
      window.callbacks.censusAPI( data, rural );
    }
    )
    .catch( function( error ) {
      if ( error ) {
        const addressElement = DT.createEl( '<li>' + address + '</li>' );

        DT.addEl( DT.getEl( '#process-error-desc' ), addressElement );
        DT.removeClass( '#process-error', 'u-hidden' );

        count.incrementTotal();
      }
    } );
}

export default callCensus;
