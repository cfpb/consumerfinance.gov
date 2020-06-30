// External modules
const AOS = require( 'aos/dist/aos' );
const cfExpandables = require( 'cf-expandables/src/Expandable' );

// Internal modules
const scroll = require( './scroll' );
const search = require( './search' );
const sticky = require( './sticky' );
const closest = require( './util/dom-traverse' ).closest;
const expandableFacets = require( './expandable-facets' );
const analytics = require( './analytics' );

const app = {
  init: () => {
    AOS.init();
    cfExpandables.init();
    expandableFacets.init();
    scroll.init();
    sticky.init();
    analytics.bindAnalytics();
  }
};

window.addEventListener( 'load', app.init );
