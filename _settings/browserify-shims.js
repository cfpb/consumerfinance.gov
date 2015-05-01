'use strict';

// Config file for adding external libraries that require browserify shimming.
module.exports = {
  jquery: { exports: 'jQuery' },
  'jquery-easing': {
    depends: {
      jquery: 'jQuery',
    }
  },
  'cf-expandables': {
    depends: {
      jquery: 'jQuery',
    }
  },
  chosen: { exports: 'chosen' },
  requestNextAnimationFrame: { exports: 'requestNextAnimationFrame' },
  slick: { exports: 'slick' }
};
