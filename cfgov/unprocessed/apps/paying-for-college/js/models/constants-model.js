import { getConstants } from '../dispatchers/get-api-values.js';

const constantsModel = {
  values: {},

  init: function() {
    getConstants()
      .then( resp => {
        const data = JSON.parse( resp.responseText );

        for ( const key in data ) {
          constantsModel.values[key] = data[key];
        }
    } );
  }

}

export {
    constantsModel
}