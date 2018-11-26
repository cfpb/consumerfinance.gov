const hud = require( './hud-util' );

/* This script uses a local Django API to acquire a list of the 10 closest
HUD Counselors by zip code. See hud_api_replace for more details on the
API queries. -wernerc */

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
let markerDomCache = {};

/* initialize_map() sets options and creates the map */
function initializeMap() {
  window.L.mapbox.accessToken = window.mapbox_access_token;
  map = window.L.mapbox.map( 'hud_hca_api_map_container', 'mapbox.streets' )
    .setView( [ 40, -80 ], 2 );

  if ( window.hud_data.counseling_agencies ) {
    updateMap( window.hud_data );
  }
}

/**
 * Cache the map marker result item DOM references so that a DOM lookup doesn't
 * happen every time a map marker is clicked. The lookup happens on the first
 * click and then is stored in the markerDomCache object.
 * @param  {number} num - The index of the result item.
 * @return {HTMLNode} The DOM node of the result item.
 */
function queryMarkerDom( num ) {
  const selector = '#hud-result-' + Number.parseInt( num, 10 );
  let cachedItem = markerDomCache[selector];
  if ( typeof cachedItem === 'undefined' ) {
    console.log( 'looking up the item!' );
    cachedItem = document.querySelector( selector );
    markerDomCache[selector] = cachedItem;
  }

  return cachedItem;
}

/* generate_google_map(data) takes the data and plots the markers, etc, on
the google map. It's called by get_counselors_by_zip(). */
function updateMap( data ) {
  // reset the map
  markerDomCache = {};
  for ( let i = 0; i < marker_array.length; i++ ) {
    map.removeLayer( marker_array[i] );
  }
  marker_array = [];
  if ( zip_marker !== null ) {
    map.removeLayer( zip_marker );
  }
  map.setZoom( 2 );
  map.setView( [ 40, -80 ] );

  if ( hud.checkHudData( data ) === true ) {
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
        const resultEntryDom = queryMarkerDom( number );
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

initializeMap();
