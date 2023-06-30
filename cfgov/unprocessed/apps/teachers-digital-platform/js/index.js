// External modules
import cfExpandables from './Expandable.js';
import expandableFacets from './expandable-facets.js';
import beforeExpandableTransitionInit from './expandable-mobile.js';

// Internal modules
import { init as searchInit } from './search.js';
import { bindAnalytics } from './tdp-analytics.js';

const app = {
  init: () => {
    /**
     * This must come before searchInit() because it will also initialize
     * cfExpandables.
     */
    beforeExpandableTransitionInit();

    searchInit();
    cfExpandables.init();
    expandableFacets.init();

    bindAnalytics();
  },
};

window.addEventListener('load', app.init);
