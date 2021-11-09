/**
 * Update the application state model, then trigger updates in views
 */
import {
  updateCostOfBorrowingChart,
  updateMakePlanChart,
  updateMaxDebtChart
} from '../dispatchers/update-view.js';
import { stateModel } from '../models/state-model.js';

const updateState = {

  /**
   * activeSection - Update the app's active section
   * @param {*} value - the value to be assigned
   * @param {Boolean} popState - true if the update is the result of a popState event
   */
  activeSection: ( value, popState ) => {
    stateModel.setActiveSection( value, popState );
    if ( value === 'make-a-plan' ) {
      updateMakePlanChart();
    } else if ( value === 'max-debt-guideline' ) {
      updateMaxDebtChart();
    } else if ( value === 'cost-of-borrowing' ) {
      updateCostOfBorrowingChart();
    }
  },

  /**
   * getStarted - Indicate that the app has been started
   * @param {Boolean} bool - true, if the app has started
   */
  getStarted: bool => {
    if ( bool === true ) {
      stateModel.setValue( 'gotStarted', true );
    }
  },

  /**
   * nextSection - Advance to application state to the next section
   */
  nextSection: () => {
    const activeSection = stateModel.values.activeSection;
    const i = stateModel.sectionOrder.indexOf( activeSection );
    if ( i !== -1 ) {
      const nextSection = stateModel.sectionOrder[i + 1];
      updateState.activeSection( nextSection );
    }
  },

  /**
   * Update the stateModel's property to be equal to value
   * @param {String} prop - The property to update
   * @param {*} value - The value to assign
   */
  byProperty: function( prop, value ) {
    stateModel.setValue( prop, value );
  },

  /**
   * pushStateToHistory - Push current application state to window.history
   */
  pushStateToHistory: () => {
    stateModel.pushStateToHistory();
  },

  /**
   * replaceStateInHistory - Replace current application state in window.history
   * @param {String} queryString - The queryString to put in the history object
   */
  replaceStateInHistory: queryString => {
    stateModel.replaceStateInHistory( queryString );
  }

};

export {
  updateState
};
