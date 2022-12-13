// External modules
const AOS = require('aos/dist/aos');
import cfExpandables from '@cfpb/cfpb-expandables/src/Expandable.js';
import expandableFacets from './expandable-facets.js';
import beforeExpandableTransitionInit from './expandable-mobile.js';

// Internal modules
import scroll from './scroll.js';
import { init as searchInit } from './search.js';
import sticky from './sticky.js';
import { bindAnalytics } from './tdp-analytics.js';
import surveys from './tdp-surveys.js';

const app = {
  init: () => {
    AOS.init();

    /**
     * This must come before searchInit() because it will also initialize
     * cfExpandables.
     */
    beforeExpandableTransitionInit();

    searchInit();
    cfExpandables.init();
    expandableFacets.init();

    scroll.init();
    sticky.init();
    surveys.init();
    bindAnalytics();
  },
};

window.addEventListener('load', app.init);
