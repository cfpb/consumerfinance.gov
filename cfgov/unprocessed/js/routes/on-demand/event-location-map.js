/* ==========================================================================
   Scripts for Event Post Preview organism.
   ========================================================================== */

import { ajaxRequest } from '../../modules/util/ajax-request';

const BASE_CLASS = 'o-post-preview_image-event-map';
const MAP_IMAGES = document.body.querySelectorAll( '.' + BASE_CLASS );
const MAPBOX_ACCESS_TOKEN = MAP_IMAGES[0].dataset.mapboxToken;

/**
 * Gets map image of given location coordinates from Mapbox
 *
 * @param {string} response JSON data response from Mapbox API
 * @param {string} el image element where src attribute goes
 * @returns {string} url for image src
 */
function getMapImage( response, el ) {
  let data = JSON.parse ( response );
  let coordinates = data.features[0].geometry.coordinates;
  let coords = {
    longitude: coordinates[0],
    latitude: coordinates[1]
  };

  let imageSrc = 'https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/' + coords.longitude + ',' + coords.latitude + ',12/270x270?access_token=' + MAPBOX_ACCESS_TOKEN;

  console.log( imageSrc );

  el.setAttribute( 'src', imageSrc);
}

function fail( ) {
  console.error( 'Failed to get location from Mapbox' );
}

/**
 * Sends a given location name to Mapbox Search API
 *
 * @param {string} locationName: event location from Wagtail field.
 *  Can be city and state or state
 * @param {string} el image element where src attribute goes
 */
function getLocation( locationName, el ) {
  let geocodeUrl = 'https://api.mapbox.com/geocoding/v5/mapbox.places/' + locationName + '.json?access_token=' + MAPBOX_ACCESS_TOKEN;

  ajaxRequest(
    'GET',
    geocodeUrl,
    {
      success: function( response ) {
        getMapImage( response, el );
      },
      fail: fail
    }
  );
}

function init( ) {
  for ( let i = 0; i < MAP_IMAGES.length; i++ ) {
    let mapEl = MAP_IMAGES[i];
    let mapLocation = mapEl.dataset.mapLocation;
    console.warn( mapEl );
    getLocation( mapLocation, mapEl );
  }
}

init();
