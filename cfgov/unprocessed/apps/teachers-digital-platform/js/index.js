// External modules
const AOS = require( 'aos/dist/aos' );
import cfExpandables from '@cfpb/cfpb-expandables/src/Expandable';

// Internal modules
const scroll = require( './scroll' );
const search = require( './search' );
const sticky = require( './sticky' );
import expandableFacets from './expandable-facets';
const analytics = require( './tdp-analytics' );

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
