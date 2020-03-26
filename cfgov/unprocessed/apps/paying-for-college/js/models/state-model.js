/**
 * This file contains the model for the application state - that is, an Object
 * which tracks the current app state and allows the views to update based on
 * state.
*/

const stateModel = {
  values: {
    activeSection: null,
    schoolSelected: null,
    gotStarted: false,
    handleCostsButtonClicked: false,
    programType: null,
    programLength: null,
    programRate: null,
    programHousing: null
  },

  init: () => {
    // PLACEHOLDER - Add more interesting stuff later
    stateModel.foo = 'bar';
  }

};

export {
  stateModel
};
