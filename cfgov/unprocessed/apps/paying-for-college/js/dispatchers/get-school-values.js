const schoolModel = require( '../models/school-model' );

const getSchoolValues = {
  values: function() {
    return schoolModel.values;
  }
};

module.exports = getSchoolValues;
