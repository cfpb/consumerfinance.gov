// This model contains school information
import { updateUrlQueryString } from '../dispatchers/update-view.js';

const schoolModel = {
  values: {},

  setValue: function( name, value ) {
    schoolModel.values[name] = value;
    updateUrlQueryString();
  }

};

export {
  schoolModel
};
