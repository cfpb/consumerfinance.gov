/**
 * Update the application state model, then trigger updates in views
 */
import { stateModel } from '../models/state-model.js';

const updateState = {
  /**
   * activeSection - Update the app's active section
   * @param {*} value - the value to be assigned
   * @param {boolean} popState - true if the update is the result of a popState event
   */
  activeSection: (value, popState) => {
    stateModel.setActiveSection(value, popState);
  },

  /**
   * getStarted - Indicate that the app has been started
   * @param {boolean} bool - true, if the app has started
   */
  getStarted: (bool) => {
    if (bool === true) {
      stateModel.setValue('gotStarted', true);
    }
  },

  /**
   * navigateTo - Advance to application state to the next section
   * @param {string} destination - the name of the section to advance to
   */
  navigateTo: (destination) => {
    updateState.activeSection(destination);
  },

  /**
   * Update the stateModel's property to be equal to value
   * @param {string} prop - The property to update
   * @param {*} value - The value to assign
   */
  byProperty: function (prop, value) {
    stateModel.setValue(prop, value);
  },

  /**
   * pushStateToHistory - Push current application state to window.history
   */
  pushStateToHistory: () => {
    stateModel.pushStateToHistory();
  },

  /**
   * replaceStateInHistory - Replace current application state in window.history
   * @param {string} queryString - The queryString to put in the history object
   */
  replaceStateInHistory: (queryString) => {
    stateModel.replaceStateInHistory(queryString);
  },
};

export { updateState };
