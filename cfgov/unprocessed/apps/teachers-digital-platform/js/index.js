// Internal modules
import { init as searchInit } from './search.js';
import { bindAnalytics } from './tdp-analytics.js';

const app = {
  init: () => {
    searchInit();
    bindAnalytics();
  },
};

window.addEventListener('load', app.init);
