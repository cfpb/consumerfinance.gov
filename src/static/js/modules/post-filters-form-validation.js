/* ==========================================================================
   #post-filters-form validation

   Checks the date range values.
   If the from (gte) date is larger than the to (lte) date, swap them.
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );

function init() {
  $( '.js-validate-filters' ).each( function() {
    var $this = $( this ),
        $gte = $this.find( '.js-filter_range-date__gte' ),
        $lte = $this.find( '.js-filter_range-date__lte' );

    // @param date1 {Date} The starting date in the range.
    // @param date2 {Date} The ending date in the range.
    // @return {Boolean} true if the ending date is after the starting date.
    function isValidDateRange( date1, date2 ) {
      return date2.getTime() > date1.getTime();
    }

    // Check that the date isn't empty,
    // and set it to the other set date if it is.
    // If it's still empty, return an empty string.
    // If year or month is missing, the current month or year are added.
    // @param targetDate {String} Date string to format.
    // @param compData {String} Other date in the date range we're checking.
    // @return {String} Formatted targetDate or an empty string.
    //   Throws an error if the expected YYYY-MM format is wrong.
    function formatDateString( targetDate, compDate ) {
      var formattedDate = targetDate === '' ? compDate : targetDate;
      if ( formattedDate === '' ) return formattedDate;

      if ( /^\d{4}$/.test( formattedDate ) ) {
        var month = String( new Date().getMonth() + 1 );
        if ( month.length !== 2 ) month = '0' + month;
        formattedDate += '-' + month;
      } else if ( /^\d{2}$/.test( formattedDate ) ) {
        var year = new Date().getFullYear();
        formattedDate = year + '-' + formattedDate;
      } else if ( /^\d{4}-\d{2}$/.test( formattedDate ) === false ) {
        var msg = 'Unexpected date format! Should be in YYYY-MM format.';
        throw new Error( msg );
      }

      return formattedDate;
    }

    $( this ).on( 'submit', function( e ) {
      var gteVal = $gte.val();
      var lteVal = $lte.val();

      var gteParsedVal = formatDateString( gteVal, lteVal );
      var lteParsedVal = formatDateString( lteVal, gteVal );

      var validDateRange = isValidDateRange(
        new Date( gteParsedVal ),
        new Date( lteParsedVal )
      );
      if ( validDateRange ) {
        $gte.val( gteParsedVal );
        $lte.val( lteParsedVal );
      } else {
        // Swap the values if "from" value comes after "to" value.
        $gte.val( lteParsedVal );
        $lte.val( gteParsedVal );
      }
    } );
  } );
}

// Expose public methods.
module.exports = { init: init };
