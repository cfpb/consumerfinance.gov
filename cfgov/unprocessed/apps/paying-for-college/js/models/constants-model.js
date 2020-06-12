import { financialModel } from './financial-model.js';
import { getConstants } from '../dispatchers/get-api-values.js';
import { updateFinancialView } from '../dispatchers/update-view.js';

// Please excuse some uses of underscore for code/HTML property clarity!
/* eslint camelcase: ["error", {properties: "never"}] */

const constantsModel = {
  values: {},
  nonNumeric: [ 'constantsYear' ],
  financialValues: {
    rate_directSub: 'subsidizedRate',
    fee_directSub: 'DLOriginationFee',
    rate_directUnsub: 'unsubsidizedRate',
    fee_directUnsub: 'DLOriginationFee',
    rate_gradPlus: 'gradPlusRate',
    fee_gradPlus: 'plusOriginationFee',
    rate_parentPlus: 'parentplusRate',
    fee_parentPlus: 'plusOriginationFee'
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
              financialModel.values[key] = constantsModel.values[rosetta];
            }
          }

          resolve( true );
        } )
        .catch( function( error ) {
          reject( error );
          // console.log( 'An error occurred!', error );
        } );
    } );
  }
};

export {
  constantsModel
};
