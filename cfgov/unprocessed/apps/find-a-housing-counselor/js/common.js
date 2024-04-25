import { checkHudData } from './hud-util.js';

const MAPBOX_JS_URL = 'https://api.mapbox.com/mapbox.js/v3.3.1/mapbox.js';
const MAPBOX_CSS_URL = 'https://api.mapbox.com/mapbox.js/v3.3.1/mapbox.css';

// Settings stored in the template from the backend.
const mapboxAccessToken = window.cfpbHudSettings.mapbox_access_token;
const hudData = window.cfpbHudSettings.hud_data;

/* This script uses a local Django API to acquire a list of the 10 closest
HUD Counselors by zip code. See hud_api_replace for more details on the
API queries. -wernerc */

// Set up print results list button functionality, if it exists.
const printPageLink = document.getElementById('hud_print-page-link');
if (printPageLink) {
  printPageLink.addEventListener('click', (evt) => {
    evt.preventDefault();
    window.print();
  });
}

let map;
let markerArray = [];
let zipMarker = null;
let markerDomCache = {};

/**
 * Dynamically add mapbox CSS to document head.
 */
function injectMapboxCSS() {
  const mapStyles = document.createElement('link');
  mapStyles.rel = 'stylesheet';
  mapStyles.href = MAPBOX_CSS_URL;
  document.head.appendChild(mapStyles);
}

/**
 * Dynamically add mapbox JavaScript to document head.
 */
function injectMapboxJS() {
  const mapScript = document.createElement('script');
  mapScript.addEventListener('load', scriptLoaded);
  mapScript.async = true;
  mapScript.src = MAPBOX_JS_URL;
  document.head.appendChild(mapScript);
}

/**
 * Event handler for successful load of mapbox JavaScript file.
 * @param {Event} evt - The event object from the load event.
 */
function scriptLoaded(evt) {
  evt.target.removeEventListener('load', scriptLoaded);
  initializeMap();
}

/**
 * Set access map options and create map.
 */
function initializeMap() {
  const showMap = Boolean(document.getElementById('hud-hca-api-map-container'));

  if (showMap) {
    const fcm = document.getElementById('hud_search_container');
    fcm.classList.remove('no-js');
    window.L.mapbox.accessToken = mapboxAccessToken;
    map = window.L.mapbox
      .map('hud-hca-api-map-container')
      .setView([40, -80], 2)
      .addLayer(
        window.L.mapbox.styleLayer('mapbox://styles/mapbox/streets-v11'),
      );

    if (hudData.counseling_agencies) {
      updateMap(hudData);
    }
  }
}

/**
 * Cache the map marker result item DOM references so that a DOM lookup doesn't
 * happen every time a map marker is clicked. The lookup happens on the first
 * click and then is stored in the markerDomCache object.
 * @param {number} num - The index of the result item.
 * @returns {HTMLElement} The DOM node of the result item.
 */
function queryMarkerDom(num) {
  const id = 'hud-result-' + Number.parseInt(num, 10);
  let cachedItem = markerDomCache[id];
  if (typeof cachedItem === 'undefined') {
    cachedItem = document.getElementById(id);
    markerDomCache[id] = cachedItem;
  }

  return cachedItem;
}

/**
 * Takes the data and plots the markers, etc, on the map.
 * @param {object} data - data returned from the API.
 */
function updateMap(data) {
  // reset the map
  markerDomCache = {};
  for (let i = 0; i < markerArray.length; i++) {
    map.removeLayer(markerArray[i]);
  }
  markerArray = [];
  if (zipMarker !== null) {
    map.removeLayer(zipMarker);
  }
  map.setZoom(2);
  map.setView([40, -80]);

  if (checkHudData(data) === true) {
    const lat = data.zip.lat;
    const lng = data.zip.lng;
    const ziplatlng = [lat, lng];
    const zoom = 14;

    map.setZoom(zoom);
    map.setView(ziplatlng);

    let xmax = -Infinity;
    let xmin = Infinity;
    let ymax = -Infinity;
    let ymin = Infinity;

    zipMarker = window.L.circle(ziplatlng, 3).addTo(map);

    data.counseling_agencies.forEach((val, i) => {
      const lat = val.agc_ADDR_LATITUDE;
      const lng = val.agc_ADDR_LONGITUDE;
      const position = new window.L.LatLng(lat, lng);

      if (lat > ymax) ymax = lat;
      if (lat < ymin) ymin = lat;
      if (lng > xmax) xmax = lng;
      if (lng < xmin) xmin = lng;

      let number = i + 1;

      if (number < 10) {
        number = '0' + number;
      }

      const icon = window.L.icon({
        iconUrl:
          '/static/apps/find-a-housing-counselor/img/hud_gmap/agc_' +
          number +
          '.png',
        iconAnchor: [14, 32],
        iconSize: [27, 32],
      });

      const marker = new window.L.Marker(position, { icon: icon }).addTo(map);
      markerArray[i] = marker;

      marker.on('click', function () {
        const resultEntryDom = queryMarkerDom(number);
        resultEntryDom.scrollIntoView({
          behavior: 'smooth',
          block: 'start',
        });
      });
    });

    // shift the max bounds so that the dropped pins are always on screen
    const xd = (xmax - xmin) / 10;
    const yd = (ymax - ymin) / 10;

    map.fitBounds([
      [ymin - yd, xmin - xd],
      [ymax + yd, xmax + xd],
    ]);
  }
}

// Get started by injecting the Mapbox CSS and JavaScript in the document head…
injectMapboxCSS();
injectMapboxJS();
