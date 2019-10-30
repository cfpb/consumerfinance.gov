// This file contains the 'view' of all financial info, including costs, loans, etc

import { updateState } from '../dispatchers/update-state.js';
import { getState } from '../dispatchers/get-state.js';

const financialView = {
  _sections: null,


  updateSection: function() {
    const activeName = getState( 'activeSection' );
    const query = '.college-costs_tool-section[data-tool-section="' + activeName + '"]';
    const activeSection = document.querySelector( query );

    this._sections.forEach( elem => {
      elem.classList.remove( 'active' );
    } );

    activeSection.classList.add( 'active' );
  },

  init: function( body ) {
    this._sections = body.querySelectorAll( '.college-costs_tool-section' );

    this.updateSection();

  }

};

export {
  financialView
};
