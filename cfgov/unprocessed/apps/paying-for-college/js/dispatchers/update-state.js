/**
 * Update the application state model, then trigger updates in views
 */
import { navigationView } from '../views/navigation-view.js';
import { stateModel } from '../models/state-model.js';

const updateState = {

  /**
   * activeSection - Change the active navigation view, trigger an update
   * for the navigationView
   *
   * @param {string} item - Value of 'data-nav_item' attribute
   */
  activeSection: item => {
    stateModel.setValue( 'activeSection', item );

    navigationView.update();
  },

  getStarted: bool => {
    if ( bool === true ) {
      stateModel.setValue( 'gotStarted', true );
    }
  },

  byProperty: function( prop, value ) {
    stateModel.setValue( prop, value );
  }

};

export {
  updateState
};
