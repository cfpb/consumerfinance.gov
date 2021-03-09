import DT from './dom-tools';

const MAPBOX_JS_URL = 'https://api.mapbox.com/mapbox.js/v3.3.1/mapbox.js';
const MAPBOX_CSS_URL = 'https://api.mapbox.com/mapbox.js/v3.3.1/mapbox.css';
const mapboxAccessToken = 'pk.eyJ1IjoiY2ZwYiIsImEiOiJodmtiSk5zIn0.VkCynzmVYcLBxbyHzlvaQw';
const mapIdString = 'mapbox://styles/mapbox/streets-v11';

let map;
const marker_array = [];
const zip_marker = null;
const markerDomCache = {};

/**
 * Dynamically add mapbox CSS to document head.
 */
function injectMapboxCSS() {
  const mapStyles = document.createElement( 'link' );
  mapStyles.rel = 'stylesheet';
  mapStyles.href = MAPBOX_CSS_URL;
  document.head.appendChild( mapStyles );
}

/**
 * Dynamically add mapbox JavaScript to document head.
 */
function injectMapboxJS() {
  const mapScript = document.createElement( 'script' );
  mapScript.addEventListener( 'load', scriptLoaded );
  mapScript.async = true;
  mapScript.src = MAPBOX_JS_URL;
  document.head.appendChild( mapScript );
}

/**
 * Event handler for successful load of mapbox JavaScript file.
 * @param  {Event} evt - The event object from the load event.
 */
function scriptLoaded( evt ) {
  evt.target.removeEventListener( 'load', scriptLoaded );
  initializeMap();
}

/**
 * Set access map options and create map.
 */
function initializeMap() {
  window.L.mapbox.accessToken = mapboxAccessToken;
}

// when a.jsLoadMap is clicked
const resultsMapDom = document.querySelector( '#results' );
resultsMapDom.addEventListener( 'click', function( evt ) {
  const target = evt.target;
  let toggleMapLink = target;
  if ( DT.hasClass( target.parentNode, 'jsLoadMap' ) ) {
    toggleMapLink = target.parentNode;
  }

  if ( DT.hasClass( toggleMapLink, 'jsLoadMap' ) ) {

    evt.preventDefault();

    // setup vars (data attributes)
    const lat = DT.getElData( toggleMapLink, 'lat' );
    const lon = DT.getElData( toggleMapLink, 'lon' );
    const id = DT.getElData( toggleMapLink, 'id' );
    const isMapShown = DT.getElData( toggleMapLink, 'map' ) === 'true';

    const parentMapRow = DT.getParentEls( toggleMapLink, 'tr' )[0];
    const mapTDs = DT.getChildEls( parentMapRow, 'td' );
    const mapRow = DT.getNextEls( parentMapRow, 'tr' )[0];
    const hasHideClass = DT.hasClass( mapRow, 'u-hidden' );

    // if the map row is hidden
    if ( hasHideClass ) {

      // show it
      DT.removeClass( mapRow, 'u-hidden' );

      // change text
      DT.changeElHTML(
        toggleMapLink,
        'Hide map <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1200" class="cf-icon-svg"><path d="M500 105.2c-276.1 0-500 223.9-500 500s223.9 500 500 500 500-223.9 500-500-223.9-500-500-500zm263.1 550.7H236c-27.6 0-50-22.4-50-50s22.4-50 50-50h527.1c27.6 0 50 22.4 50 50s-22.4 50-50 50z"></path></svg>'
      );

      // only show initiate the map the first time
      if ( isMapShown === false ) {

        // set the map to true (won't try to initate again)
        toggleMapLink.setAttribute( 'data-map', true );

        DT.nextFrame( function() {
          const latlng = window.L.latLng( lon, lat );
          const map = window.L.mapbox.map( id )
            .setView( latlng, 12 )
            .addLayer( window.L.mapbox.styleLayer( mapIdString ) );
          map.dragging.disable();
          map.touchZoom.disable();
          map.doubleClickZoom.disable();
          map.scrollWheelZoom.disable();

          if ( map.tap ) {
            map.tap.disable();
          }

          // add marker
          const marker = window.L.marker( latlng ).addTo( map );
        } );
      }
    } else { // map is being displayed

      // hide it
      DT.addClass( mapRow, 'u-hidden' );

      // change text
      DT.changeElHTML(
        toggleMapLink,
        'Show map <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1200" class="cf-icon-svg"><path d="M500 105.2c-276.1 0-500 223.9-500 500s223.9 500 500 500 500-223.9 500-500-223.9-500-500-500zm263.1 550.7H549.6v213.6c0 27.6-22.4 50-50 50s-50-22.4-50-50V655.9H236c-27.6 0-50-22.4-50-50s22.4-50 50-50h213.6V342.3c0-27.6 22.4-50 50-50s50 22.4 50 50v213.6h213.6c27.6 0 50 22.4 50 50s-22.5 50-50.1 50z"></path></svg>'
      );
    }
  }
} );

// Get started by injecting the Mapbox CSS and JavaScript in the document head…
injectMapboxCSS();
injectMapboxJS();
