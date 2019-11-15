/**
 * This file contains the model for the application state - that is, an Object
 * which tracks the current app state and allows the views to update based on
 * state.
*/

const stateModel = {
  activeSection: null,
  schoolSelected: null,
  gotStarted: false,


  init: () => {
    // PLACEHOLDER - Add more interesting stuff later
    stateModel.foo = 'bar';
  }

};

export {
  stateModel
};
