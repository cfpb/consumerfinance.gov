import benefitsModel from '../models/benefits-model';
import lifetimeModel from '../models/lifetime-model';

const update = {

  /**
   * This function updates properties of the benefits model.
   * @param {string} prop - The property to be updated.
   * @param {number|string} val - The new value of the property.
   */
  benefits: function( prop, val ) {
    benefitsModel.values[prop] = val;
  },
  lifetime: function( prop, val ) {
    lifetimeModel.values[prop] = val;
  },

  /**
   * This function takes a response from an AJAX call and processes
   * the response into the benefits model.
   * @param {object} resp - The AJAX response object.
   */
  processApiData: function( resp ) {
    const data = resp.data;
    let fullAge = Number( data['full retirement age'].substr( 0, 2 ) );
    if ( resp.currentAge > fullAge ) {
      fullAge = resp.currentAge;
    }

    for ( const benKey in resp.data.benefits ) {
      if ( {}.hasOwnProperty.call( resp.data.benefits, benKey ) &&
           benKey.substr( 0, 3 ) === 'age' ) {
        const prop = benKey.replace( ' ', '' );
        update.benefits( prop, resp.data.benefits[benKey] );
      }
    }
    for ( const lifeKey in resp.data.lifetime ) {
      if ( {}.hasOwnProperty.call( resp.data.lifetime, lifeKey ) ) {
        update.lifetime( lifeKey, resp.data.lifetime[lifeKey] );
      }
    }

    update.benefits( 'currentAge', resp.current_age );
    update.benefits( 'past_fra', resp.past_fra );
    update.benefits( 'fullRetirementAge', data['full retirement age'] );
    update.benefits( 'earlyRetirementAge', data['early retirement age'] );
    update.benefits( 'fullAge', fullAge );
    update.benefits(
      'earlyAge',
      Number( data['early retirement age'].substr( 0, 2 ) )
    );
    update.benefits(
      'monthsPastBirthday',
      Number( data.months_past_birthday )
    );
  }

};

export default update;
