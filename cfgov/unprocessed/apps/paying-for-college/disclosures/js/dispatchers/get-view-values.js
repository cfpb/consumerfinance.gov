// TODO: Remove jquery.
const $ = require( 'jquery' );

const stringToNum = require( '../utils/handle-string-input' );

const getViewValues = {
  def: 0,

  init: function( apiValues ) {
    return $.extend( this.inputs(), apiValues );
  },

  getPrivateLoans: function( values ) {
    // Note: Only run once, during init()
    const $privateLoans = $( '[data-private-loan]' );
    values.privateLoanMulti = [];
    $privateLoans.each( function() {
      const $ele = $( this );
      const $fields = $ele.find( '[data-private-loan_key]' );
      const loanObject = { amount: 0, totalLoan: 0, rate: 0, deferPeriod: 0 };
      $fields.each( function() {
        const key = $( this ).attr( 'data-private-loan_key' );
        let value = $( this ).val();
        if ( key === 'rate' ) {
          value /= 100;
        }
        loanObject[key] = stringToNum( value );
      } );
      values.privateLoanMulti.push( loanObject );
    } );
    return values;
  },

  inputs: function() {
    // Note: Only run once, during init()
    let values = {};
    const $elements = $( '[data-financial]' );

    $elements.not( '[data-private-loan_key]' ).each( function() {
      const name = $( this ).attr( 'data-financial' );
      values[name] = stringToNum( $( this ).val() ) || 0;
      if ( $( this ).attr( 'data-percentage_value' ) === 'true' ) {
        values[name] /= 100;
      }
    } );

    values = this.getPrivateLoans( values );
    return values;
  }
};

module.exports = getViewValues;
