/**
 * Update the application state model, then trigger updates in views
 */
import { stateModel } from '../models/state-model.js';
import { navigationView } from '../views/navigation-view.js';
import { financialView } from '../views/financial-view.js';
import { schoolView } from '../views/school-view.js';

const updateState = {

  /**
   * activeSection - Change the active navigation view, trigger an update
   * for the navigationView
   *
   * @param {string} item - Value of 'data-nav_item' attribute
   */
  activeSection: item => {
    stateModel.activeSection = item;

    navigationView.update();
  },

  getStarted: bool => {
    if ( bool === true ) {
      stateModel.gotStarted = true;
    }
  }

};

export {
  updateState
};
