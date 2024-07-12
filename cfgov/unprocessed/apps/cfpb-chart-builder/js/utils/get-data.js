import ajax from 'xdr';
import cache from './session-storage';

let DATA_SOURCE_BASE = 'https://files.consumerfinance.gov/data/';

const getData = sources => {

  // Let browsers override the data source root (useful for localhost testing).
  DATA_SOURCE_BASE = window.CFPB_CHART_DATA_SOURCE_BASE || DATA_SOURCE_BASE;

  const urls = sources.split( ';' );

  const promises = urls.map( url => new Promise( ( resolve, reject ) => {

    // Only prepend the data source base if it's a relative URL.
    if ( url.indexOf( 'http' ) !== 0 && url.indexOf( '/' ) !== 0 ) {
      url = DATA_SOURCE_BASE + url.replace( '.csv', '.json' );
    }

    if ( cache.getItem( url ) ) {
      /* Ensure UI isn't blocked when loading large shapefiles by making
         cache resolver asynchronous https://stackoverflow.com/q/10180391 */
      return setTimeout( () => resolve( cache.getItem( url ) ), 0 );
    }

    return ajax( { url: url, type: 'json' }, function( resp ) {
      if ( resp.error ) {
        reject( resp.error );
        return;
      }
      cache.setItem( url, resp.data );
      resolve( resp.data );
    } );
  } ) );

  return Promise.all( promises );
};

export default getData;
