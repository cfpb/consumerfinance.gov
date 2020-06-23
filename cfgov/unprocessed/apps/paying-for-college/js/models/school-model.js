// This model contains school information
import { decimalToPercentString } from '../util/number-utils.js';
import { updateState } from '../dispatchers/update-state.js';
import { updateUrlQueryString } from '../dispatchers/update-view.js';

const schoolModel = {
  values: {},
  textPercents: [ 'defaultRate', 'rateGraduation', 'rateRepay3yr' ],

  setValue: function( name, value ) {
    schoolModel.values[name] = value;

    if ( schoolModel.textPercents.indexOf( name ) !== -1 ) {
      const key = name + 'Text';
      schoolModel.values[key] = decimalToPercentString( value, 1 );
    }

    // Alert the state model to school control
    if ( name === 'control' ) {
      updateState.byProperty( 'schoolControl', value );
    }

    updateUrlQueryString();
  }

};

export {
  schoolModel
};
