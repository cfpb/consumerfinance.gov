/* ==========================================================================
   Pagination Form validation
   Check to verify page input value is number and within min/max range
   before submitting form.
   ========================================================================== */

'use strict';

// Import modules
var $ = require( 'jquery' );

/**
 * Set up DOM references and event handlers.
 */
function init() {
  $( '.js-validate_pagination' ).each( function() {
    var $form = $( this );
    var $placeHolder;

    $form.on( 'submit', function() {
      var formIsValid = false;
      var $pageInput = $form.find( '#pagination_current-page' );
      var pageVal = $pageInput.val();
      var pageMinVal = parseInt( $pageInput.attr( 'min' ), 10 );
      var pageMaxVal = parseInt( $pageInput.attr( 'max' ), 10 );

      formIsValid = isNaN( pageVal ) === false &&
                    pageVal >= pageMinVal &&
                    pageVal <= pageMaxVal;

      if ( formIsValid === false ) {

        if ( typeof $placeHolder === 'undefined' ) {
          $placeHolder = $( '<div class=\'cf-notification__pagination-ctr\'></div>' );
          $form.parents( 'nav.pagination' ).after( $placeHolder );
          $( $placeHolder ).cf_notifier();
        }

        $placeHolder.trigger( 'cf_notifier:notify', {
          message: 'Please enter a valid page number.',
          state:   'error'
        } );
      }

      return formIsValid;
    } );

    return $form;
  } );
}

// Expose public methods.
module.exports = {
  init: init
};
