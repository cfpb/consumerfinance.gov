import { updateFinancial } from '../dispatchers/update-models.js';
import { updateState } from '../dispatchers/update-state.js';
import { getConstants } from '../dispatchers/get-api-values.js';

// Please excuse some uses of underscore for code/HTML property clarity!
/* eslint camelcase: ["error", {properties: "never"}] */

const constantsModel = {
  values: {
    subCaps: {
      yearOne: 0,
      yearTwo: 0,
      yearThree: 0
    },
    totalCaps: {
      yearOne: 0,
      yearTwo: 0,
      yearThree: 0
    },
    totalIndepCaps: {
      yearOne: 0,
      yearTwo: 0,
      yearThree: 0
    },
    existingDebtRate: 0.04
  },
  nonNumeric: [ 'constantsYear' ],
  financialValues: {
    rate_directSub: 'subsidizedRate',
    fee_directSub: 'DLOriginationFee',
    rate_directUnsub: 'unsubsidizedRate',
    fee_directUnsub: 'DLOriginationFee',
    rate_gradPlus: 'gradPlusRate',
    fee_gradPlus: 'plusOriginationFee',
    rate_parentPlus: 'parentplusRate',
    fee_parentPlus: 'plusOriginationFee',
    rate_existingDebt: 'existingDebtRate'
  },

  init: function() {
    return new Promise( ( resolve, reject ) => {
      getConstants()
        .then( resp => {
          const data = JSON.parse( resp.responseText );

          for ( const key in data ) {
            if ( data.hasOwnProperty( key ) ) {
              let value = data[key];
              if ( constantsModel.nonNumeric.indexOf( key ) === -1 ) {
                value = Number( value );
              }
              constantsModel.values[key] = value;
            }
          }

          for ( const key in constantsModel.financialValues ) {
            if ( constantsModel.financialValues.hasOwnProperty( key ) ) {
              const rosetta = constantsModel.financialValues[key];
              updateFinancial( key, constantsModel.values[rosetta], false );
            }
          }

          // add useful properties
          constantsModel.values.subCaps = {
            yearOne: constantsModel.values.subsidizedCapYearOne,
            yearTwo: constantsModel.values.subsidizedCapYearTwo,
            yearThree: constantsModel.values.subsidizedCapYearThree
          };
          constantsModel.values.totalCaps = {
            yearOne: constantsModel.values.unsubsidizedCapYearOne,
            yearTwo: constantsModel.values.unsubsidizedCapYearTwo,
            yearThree: constantsModel.values.unsubsidizedCapYearThree
          };
          constantsModel.values.totalIndepCaps = {
            yearOne: constantsModel.values.unsubsidizedCapIndepYearOne,
            yearTwo: constantsModel.values.unsubsidizedCapIndepYearTwo,
            yearThree: constantsModel.values.unsubsidizedCapIndepYearThree
          };

          updateState.byProperty( 'constantsLoaded', true );

          resolve( true );
        } )
        .catch( function( error ) {
          reject( error );
          console.log( 'An error occurred when accessing the constants API', error );
        } );
    } );
  }
};

export {
  constantsModel
};
