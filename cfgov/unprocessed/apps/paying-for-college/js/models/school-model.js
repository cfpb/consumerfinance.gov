// This model contains school information
import { updateUrlQueryString } from '../dispatchers/update-view.js';
import { decimalToPercentString } from '../util/number-utils.js';

const schoolModel = {
  values: {},
  textPercents: [ 'defaultRate', 'rateGraduation', 'rateRepay3yr' ],

  setValue: function( name, value ) {
    schoolModel.values[name] = value;

    if ( schoolModel.textPercents.indexOf( name ) !== -1 ) {
    	const key = name + 'Text';
    	schoolModel.values[key] = decimalToPercentString( value, 1 );
    }

    updateUrlQueryString();
  }

};

export {
  schoolModel
};
