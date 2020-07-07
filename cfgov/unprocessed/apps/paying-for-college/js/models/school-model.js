// This model contains school information
import { decimalToPercentString } from '../util/number-utils.js';
import { updateState } from '../dispatchers/update-state.js';
import { updateUrlQueryString } from '../dispatchers/update-view.js';

const schoolModel = {
  values: {
  },

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
  },

  /**
   * Returns an array of Objects which is alphabetized
   * by program name
   * @param {string} level - program level - 'undergrad' or 'graduate'
   * @returns {array} an array of objects containing program data
   */
  getAlphbeticalProgramList: function( level ) {
    let list = [];
    if ( !schoolModel.values.hasOwnProperty( 'programCodes' ) ) return list;
    if ( !schoolModel.values.programCodes.hasOwnProperty( level ) ) return list;

    list = schoolModel.values.programCodes[level].sort( ( a, b ) => {
      if ( a.name < b.name ) { return -1; } else if ( a.name > b.name ) { return 1; } else if ( b.name === a.name ) {
        if ( a.level < b.level ) return -1;
        else if ( a.level > b.level ) return 1;
      }
      return 0;
    } );

    return list;
  }

};

export {
  schoolModel
};
