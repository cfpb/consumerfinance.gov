/* ==========================================================================
   Date Range Formatter
   ========================================================================== */

'use strict';

var _dateFormat = require( 'dateformat' );
var _extend = require( './shallow-extend' ).extend;
var _uTc = require( './type-checkers' );
var _isDate = _uTc.isDate;

var _defaults = {
      dateFormat:         'yyyy-mm-dd',
      fillRangeStartDate: new Date( '01/01/2011' ),
      fillRangeEndDate:   new Date(),
      fillRangeFlag:      true,
      sortRangeFlag:      true,
      dateRange: {
        startDate: '',
        endDate:   '',
        isValid: true
      }
    };

var _properties = {};

/**
* @param {date} startDate The starting date in the range.
* @param {date} endDate The ending date in the range.
* @param {object} options An object with date in the range.
* @returns {object} An object with startDate and endDate properties.
*/
function format( startDate, endDate, options ) {
  _extend( _properties, _defaults, options || {} );
  var dateRange = _properties.dateRange;
  var steps = [];
  var stepsResult;

  if ( !( startDate || endDate ) ) return dateRange;

  if ( _properties.fillRangeFlag ) {
    steps.push( [ _fillDateRange, startDate, endDate ] );
  }

  steps.push( [ _createDateRange, _properties.sortRangeFlag ] );
  steps.push( [ _formatDateRange, _properties.dateFormat ] );
  stepsResult = _processSteps( steps );

  dateRange.startDate = stepsResult[0];
  dateRange.endDate = stepsResult[1];

  return dateRange;
}

/**
* @param {array} stepsArray An array of functions with params.
* @returns {object} Indicates success or failure of process.
*/
function _processSteps( stepsArray ) {
  var step;
  var stepFunc;
  var stepResult = [];

  for ( var i = 0; i < stepsArray.length; i++ ) {
    step = stepsArray[i];
    stepFunc = step.shift();
    stepResult = stepResult.concat( step );
    if ( _properties.dateRange.isValid === false ) {
      break;
    }

    stepResult = stepFunc.apply( null, stepResult );
  }

  return stepResult;
}

/**
* @param {date|string} date A date string or Date object.
* @returns {date} Date object.
*/
function _getDateObject( date ) {
  var _dateObject = date;

  if ( _isDate( date ) === false ) {
    _dateObject = new Date( date );
    _dateObject = _dateObject.getTime() +
                  _dateObject.getTimezoneOffset() * 60000;
    _dateObject = new Date( _dateObject );

    // Second check is necessary to capture
    // invalid dates.
    if ( _isDate( _dateObject ) === false ||
         isNaN( _dateObject.getTime() ) ) {
      _properties.dateRange.isValid = false;
    }
  }

  return _dateObject;
}

/**
* @param {date|string} startDate The starting date in the range.
* @param {date|string} endDate The ending date in the range.
* @returns {array} An object with startDate and endDate elements.
*/
function _fillDateRange( startDate, endDate ) {
  var _startDate = startDate;
  var _endDate = endDate;

  if ( _uTc.isEmpty( startDate ) && endDate ) {
    _startDate = _properties.fillRangeStartDate;
  }

  if ( _uTc.isEmpty( endDate ) && startDate ) {
    _endDate = _properties.fillRangeEndDate;
  }

  return [ _startDate, _endDate ];
}

/**
* @param {date|string} startDate The starting date in the range.
* @param {date|string} endDate The ending date in the range.
* @param {string} dateFormat A string representing the date format.
* @returns {array} An object with startDate and endDate elements.
*/
function _formatDateRange( startDate, endDate, dateFormat ) {
  return [
          _dateFormat( startDate, dateFormat ),
          _dateFormat( endDate, dateFormat )
         ];
}

/**
* @param {date|string} startDate The starting date in the range.
* @param {date|string} endDate The ending date in the range.
* @param {boolean} sortRangeFlag Flag indicating whether to sort the range.
* @returns {array} An object with sorted startDate and endDate elements.
*/
function _createDateRange( startDate, endDate, sortRangeFlag ) {
  var _startDate = startDate && _getDateObject( startDate );
  var _endDate = endDate && _getDateObject( endDate );
  var _sortRangeFlag = sortRangeFlag === true &&
                       _isDate( _startDate ) &&
                       _isDate( _endDate );
  var _dateRange = [ _startDate, _endDate ];

  if ( _sortRangeFlag && _startDate.getTime() > _endDate.getTime() ) {
    _dateRange = [ _endDate, _startDate ];
  }

  return _dateRange;
}

// Expose public methods.
module.exports = { format: format };
