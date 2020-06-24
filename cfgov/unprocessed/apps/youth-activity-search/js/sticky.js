const Stickyfill = require( 'stickyfilljs' );

const sticky = {
  init: () => {
    let stickies = document.querySelectorAll( '[data-sticky]' );

    Stickyfill.add( stickies );
  }
};

module.exports = sticky;
