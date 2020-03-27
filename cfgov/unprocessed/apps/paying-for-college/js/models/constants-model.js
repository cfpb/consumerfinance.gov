import { financialModel } from './financial-model.js';
import { getConstants } from '../dispatchers/get-api-values.js';
import { updateFinancialView } from '../dispatchers/update-view.js';

const constantsModel = {
  values: {},
  nonNumeric: [],
  financialValues: {
    rate_directSub: 'subsidizedRate',
    fee_directSub: 'DLOriginationFee',
    rate_directUnsub: 'unsubsidizedRate',
    fee_directUnsub: 'DLOriginationFee',
    rate_gradPlus: 'gradPlusRate',
    fee_gradPlus: 'plusOriginationFee'
  },

  init: function() {
    getConstants()
      .then( resp => {
        const data = JSON.parse( resp.responseText );

        for ( const key in data ) {
          let value = data[key];
          if ( constantsModel.nonNumeric.indexOf( key ) === -1 ) {
            value = Number( value );
          }
          constantsModel.values[key] = value;
        }

        for ( const key in constantsModel.financialValues ) {
          const rosetta = constantsModel.financialValues[key];
          financialModel.values[key] = constantsModel.values[rosetta];
        }

        updateFinancialView();

      } );
  }

};

export {
  constantsModel
};
