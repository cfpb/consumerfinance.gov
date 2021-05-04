import update from './update-model';

// TODO: remove jquery.
import $ from 'jquery';

const fetch = {
  apiData: function( birthdate, salary, dataLang ) {
    let url;
    if ( dataLang === 'es' ) {
      url = '../../retirement-api/estimator/' +
            birthdate + '/' + Number( salary ) + '/es/';
    } else {
      url = '../retirement-api/estimator/' +
            birthdate + '/' + Number( salary ) + '/';
    }

    const apiDataRequest = $.ajax( {
      url: url,
      dataType: 'json',
      success: function( resp ) {
        if ( resp.error === '' ) {
          update.processApiData( resp );
        }
        return resp;
      }
    } );

    return apiDataRequest;
  }
};

export default fetch;
