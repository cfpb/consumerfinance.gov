let UNDEFINED;

/* This script uses a local Django API to acquire a list of the 10 closest
HUD Counselors by zip code. See hud_api_replace for more details on the
API queries. -wernerc */

/* checkZip() is an easy, useful function that takes a string
and returns true if it's a valid zip code, or returns false.
NOTE: 'Valid' means 5 numeric characters,
not necessarily 'existant' and 'actually addressable.' */
function checkZip( zip ) {
  if ( zip === null || zip === UNDEFINED || zip === false ) {
    return false;
  }

  zip = zip.toString().replace( /[^0-9]+/g, '' );
  zip = zip.slice( 0, 5 );
  if ( zip.length === 5 ) {
    return true;
  }

  return false;
}

/* checkHudData() just makes sure your data has the correct structure
before you start requesting properties that don't exist in
generate_html() and updateMap() */
function checkHudData( data ) {
  if ( data === null || data === 0 || data === UNDEFINED ) {
    return false;
  } else if ( data.hasOwnProperty( 'error' ) ||
              !data.hasOwnProperty( 'counseling_agencies' ) ||
              !data.hasOwnProperty( 'zip' ) ) {
    return false;
  }

  return true;
}

/**
 * Returns the value in a URL query string key/value pair.
 * @param  {string} key - The key in the query string to search for.
 * @returns {string} The value to return.
 */
function getURLQueryVariable( key ) {
  const query = window.location.search.substring( 1 );
  const vars = query.split( '&' );
  let pair;
  for ( let i = 0, len = vars.length; i < len; i++ ) {
    pair = vars[i].split( '=' );
    if ( decodeURIComponent( pair[0] ) === key ) {
      return decodeURIComponent( pair[1] );
    }
  }

  return '';
}

// Set up print results list button functionality, if it exists.
const printPageLink = document.querySelector( '#hud_print-page-link' );
if ( printPageLink ) {
  printPageLink.addEventListener( 'click', evt => {
    evt.preventDefault();
    window.print();
  } );
}

let map;
let marker_array = [];
let zip_marker = null;

/* initialize_map() sets options and creates the map */
function initializeMap() {
  window.L.mapbox.accessToken = window.mapbox_access_token;
  map = window.L.mapbox.map( 'hud_hca_api_map_container', 'mapbox.streets' )
    .setView( [ 40, -80 ], 2 );

  if ( window.hud_data.counseling_agencies ) {
    updateMap( window.hud_data );
  }
}

/* generate_google_map(data) takes the data and plots the markers, etc, on
the google map. It's called by get_counselors_by_zip(). */
function updateMap( data ) {
  // reset the map
  for ( let i = 0; i < marker_array.length; i++ ) {
    map.removeLayer( marker_array[i] );
  }
  marker_array = [];
  if ( zip_marker !== null ) {
    map.removeLayer( zip_marker );
  }
  map.setZoom( 2 );
  map.setView( [ 40, -80 ] );

  if ( checkHudData( data ) === true ) {
    const lat = data.zip.lat;
    const lng = data.zip.lng;
    const ziplatlng = [ lat, lng ];
    const zoom = 14;

    map.setZoom( zoom );
    map.setView( ziplatlng );

    const bounds = map.getBounds();
    let xmax = -Infinity;
    let xmin = Infinity;
    let ymax = -Infinity;
    let ymin = Infinity;

    zip_marker = window.L.circle( ziplatlng, 3 ).addTo( map );

    data.counseling_agencies.forEach( ( val, i ) => {
      const lat = val.agc_ADDR_LATITUDE;
      const lng = val.agc_ADDR_LONGITUDE;
      const position = new window.L.LatLng( lat, lng );

      if ( lat > ymax ) ymax = lat;
      if ( lat < ymin ) ymin = lat;
      if ( lng > xmax ) xmax = lng;
      if ( lng < xmin ) xmin = lng;

      let number = i + 1;

      if ( number < 10 ) {
        number = '0' + number;
      }

      const icon = window.L.icon( {
        iconUrl: '/static/apps/find-a-housing-counselor/img/hud_gmap/agc_' + number + '.png',
        iconAnchor: [ 20, 50 ]
      } );

      const marker = new window.L.Marker( position, { icon: icon } ).addTo( map );
      marker_array[i] = marker;

      marker.on( 'click', function() {
        const resultEntryDom = document.querySelector(
          '#hud-result-' + Number.parseInt( number, 10 )
        );
        resultEntryDom.scrollIntoView( {
          behavior: 'smooth',
          block: 'start'
        } );
      } );
    } );

    // shift the max bounds so that the dropped pins are always on screen
    const xd = ( xmax - xmin ) / 10;
    const yd = ( ymax - ymin ) / 10;

    map.fitBounds( [ [ ymin - yd, xmin - xd ], [ ymax + yd, xmax + xd ] ] );
  }
}

// If there is a GET value for zip, load that zip immediately.
const getzip = getURLQueryVariable( 'zipcode' );
if ( getzip !== '' ) {
  document.querySelector( '#hud_hca_api_query' ).value = getzip;
}

module.exports = {
  initializeMap,
  checkZip,
  checkHudData,
  getURLQueryVariable
};
