// This file contains the model for after-college expenses

const expensesModel = {
  values: {},

  /**
   * setValue - Used to set a value
   * @param {String} name - Property name
   * @param {Number} value - New value of property
   */
  setValue: ( name, value ) => {
    expensesModel.values[name] = value;
  }
};

export {
  expensesModel
};
