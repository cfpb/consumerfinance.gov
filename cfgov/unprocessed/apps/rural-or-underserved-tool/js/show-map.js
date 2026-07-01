import {
  removeClass,
  addClass,
  hasClass,
  nextFrame,
  changeElHTML,
  getElData,
  getParentEls,
  getNextEls,
} from './dom-tools.js';

const MAPBOX_JS_URL = 'https://api.mapbox.com/mapbox.js/v3.3.1/mapbox.js';
const MAPBOX_CSS_URL = 'https://api.mapbox.com/mapbox.js/v3.3.1/mapbox.css';
const mapIdString = 'mapbox://styles/mapbox/streets-v11';

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
  window.L.mapbox.accessToken = window.cfpbMapboxAccessToken;
}

// when a.js-load-map is clicked
const resultsMapDom = document.querySelector('#results');
resultsMapDom.addEventListener('click', function (evt) {
  const target = evt.target;
  const linkText = target;
  let toggleMapLink = target.parentNode;
  if (hasClass(target.parentNode, 'js-load-map')) {
    toggleMapLink = target.parentNode;
  }
  const icon = toggleMapLink.querySelector('cfpb-icon');

  if (hasClass(toggleMapLink, 'js-load-map')) {
    evt.preventDefault();

    // setup vars (data attributes)
    const lat = getElData(toggleMapLink, 'lat');
    const lon = getElData(toggleMapLink, 'lon');
    const id = getElData(toggleMapLink, 'id');
    const isMapShown = getElData(toggleMapLink, 'map') === 'true';

    const parentMapRow = getParentEls(toggleMapLink, 'tr')[0];
    // const mapTDs = getChildEls( parentMapRow, 'td' );
    const mapRow = getNextEls(parentMapRow, 'tr')[0];
    const hasHideClass = hasClass(mapRow, 'u-hidden');

    // if the map row is hidden
    if (hasHideClass) {
      // show it
      removeClass(mapRow, 'u-hidden');

      // change text
      changeElHTML(linkText, `Hide map`);
      icon.setAttribute('name', 'minus-round');

      // only show initiate the map the first time
      if (isMapShown === false) {
        // set the map to true (won't try to initate again)
        toggleMapLink.setAttribute('data-map', true);

        nextFrame(function () {
          const latlng = window.L.latLng(lon, lat);
          const map = window.L.mapbox
            .map(id)
            .setView(latlng, 12)
            .addLayer(window.L.mapbox.styleLayer(mapIdString));
          map.dragging.disable();
          map.touchZoom.disable();
          map.doubleClickZoom.disable();
          map.scrollWheelZoom.disable();

          if (map.tap) {
            map.tap.disable();
          }

          // add marker
          window.L.marker(latlng).addTo(map);
        });
      }
    } else {
      // map is being displayed

      // hide it
      addClass(mapRow, 'u-hidden');

      // change text
      changeElHTML(linkText, `Show map`);
      icon.setAttribute('name', 'plus-round');
    }
  }
});

// Get started by injecting the Mapbox CSS and JavaScript in the document head…
injectMapboxCSS();
injectMapboxJS();
