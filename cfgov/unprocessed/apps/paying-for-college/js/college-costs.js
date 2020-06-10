// This file controls the college costs application

import { stateModel } from './models/state-model.js';
import { navigationView } from './views/navigation-view.js';

/* init() - Initialize the app */

const init = function() {
  const body = document.querySelector( 'body' );
  stateModel.init();
  navigationView.init( body );

  // For navigation testing purposes:
  document.querySelector( 'button.btn__next-step' ).removeAttribute( 'disabled' );
};


window.addEventListener( 'load', init );
