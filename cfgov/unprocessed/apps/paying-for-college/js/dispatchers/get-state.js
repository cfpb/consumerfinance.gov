/**
 * getState is used to retrieve application state from the application
 * state model
 */

import { stateModel } from '../models/state-model.js';

/**
 * getState - gets the property from the application state model
 *
 * @param {string} prop - The property name
 *
 * @returns {string} The value of the property in the stateModel Object
 */
const getState = function( prop ) {
  if ( stateModel.hasOwnProperty( prop ) ) {
    return stateModel[prop];
  }
  return false;

};

export {
  getState
};
