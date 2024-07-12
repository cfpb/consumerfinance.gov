import cache from './session-storage';
import getData from './get-data';

const DATA_SOURCE_BASE = 'https://files.consumerfinance.gov/data/';

const shapes = {
  states: `${ DATA_SOURCE_BASE }mortgage-performance/meta/us-states.geo.json`,
  metros: `${ DATA_SOURCE_BASE }mortgage-performance/meta/us-metros.geo.json`,
  counties: `${ DATA_SOURCE_BASE }mortgage-performance/meta/us-counties.geo.json`
};

const fetchMapShapes = geoType => {

  // If the shapes have already been downloaded resolve the promise immediately.
  if ( cache.getItem( `shapes-${ geoType }` ) ) {
    return Promise.resolve( cache.getItem( `shapes-${ geoType }` ) );
  }

  // Otherwise, download the shapes and cache them for future requests.
  const promise = getData( shapes[geoType] );

  promise.then( data => {
    cache.setItem( `shapes-${ geoType }`, data );
  } );

  return promise;
};

export default fetchMapShapes;
