// External modules
const AOS = require( 'aos/dist/aos' );
import cfExpandables from '@cfpb/cfpb-expandables/src/Expandable';
import expandableFacets from './expandable-facets';
import beforeExpandableTransitionInit from './expandable-mobile';

// Internal modules
const scroll = require( './scroll' );
const search = require( './search' );
const sticky = require( './sticky' );
const analytics = require( './tdp-analytics' );

const app = {
  init: () => {
    AOS.init();

    // Must come before search.init() because it will also initialize
    // cfExpandables.
    beforeExpandableTransitionInit();

    search.init();
    cfExpandables.init();
    expandableFacets.init();

    scroll.init();
    sticky.init();
    analytics.bindAnalytics();
  }
};

window.addEventListener( 'load', app.init );
