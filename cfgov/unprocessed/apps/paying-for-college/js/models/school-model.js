// This model contains school information

const schoolModel = {
  values: {},

  createSchoolProperty: function( name, value ) {
    if ( !schoolModel.values.hasOwnProperty( name ) ) {
      schoolModel.values[name] = value;
    }  
  },

  setValue: function( name, value ) {
    if ( schoolModel.values.hasOwnProperty( name ) ) {
      schoolModel.values[name] = value;
    }  
  }

};

export {
  schoolModel
};
