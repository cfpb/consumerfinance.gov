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
  // See versions at https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb
  const apiVersion = 'tigerWMS_ACS2019';
  const url = 'https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/' +
              apiVersion + '/MapServer/' +
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
