const Stickyfill = require( 'stickyfilljs' );

const sticky = {
  init: () => {
    const stickies = document.querySelectorAll( '[data-sticky]' );

    Stickyfill.add( stickies );
  }
};

module.exports = sticky;
