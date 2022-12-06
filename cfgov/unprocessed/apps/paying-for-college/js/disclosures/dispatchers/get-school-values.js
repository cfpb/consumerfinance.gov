import schoolModel from '../models/school-model.js';

const getSchoolValues = {
  values: function () {
    return schoolModel.values;
  },
};

module.exports = getSchoolValues;
