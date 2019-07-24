require( 'es6-promise' ).polyfill();
const jsonP = require( 'jsonp-p' ).default;

/**
 * Call the Census geospatial API.
 * @param {number} x - Latitude.
 * @param {number} y - Longitude.
 * @param {string} layer - Layer ID.
 * @returns {Promise} A promise returned from the API.
 */
function callTiger( x, y, layer ) {
  const url = 'https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_Current/MapServer/' +
              layer +
              '/query' +
              '?geometryType=esriGeometryPoint' +
              '&geometry=' + x + ',' + y +
              '&inSR=4326' +
              '&spatialRel=esriSpatialRelIntersects' +
              '&returnCountOnly=false' +
              '&returnIdsOnly=false' +
              '&returnGeometry=false' +
              '&outFields=*' +
              '&f=json';

  return jsonP( url ).promise;
}

export default callTiger;
