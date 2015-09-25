'use strict';
var chai = require( 'chai' );
var expect = chai.expect;
var dateRange = require(
  '../../../../cfgov/v1/preprocessed/js/modules/util/date-range-formatter.js'
);

var dateStart = new Date( '01/01/2014' );
var dateEnd = new Date( '12/31/2014' );
var fakeDateStart = '01/01/2014';
var fakeDateEnd = '12/31/2014';
var notDate = 'foo';

describe( 'dateRangeFormatter', function() {
  it( 'should transform dates to yyyy-mm-dd format by default', function() {
    expect(
      dateRange.format( dateStart, dateEnd )
    ).to.have.property( 'startDate', '2014-01-01' );

    expect(
      dateRange.format( dateStart, dateEnd )
    ).to.have.property( 'isValid', true );
  } );

  it( 'should transform date-like strings to yyyy-mm-dd', function() {
    expect(
      dateRange.format( fakeDateStart, fakeDateEnd )
    ).to.have.property( 'startDate', '2014-01-01' );

    expect(
      dateRange.format( fakeDateStart, fakeDateEnd )
    ).to.have.property( 'isValid', true );
  } );

  it( 'isValid property should return false when given non-dates', function() {
    expect(
      dateRange.format( notDate, notDate )
    ).to.have.property( 'isValid', false );
  } );

  it( 'should still work when presented with only a start date', function() {
    expect(
      dateRange.format( dateStart )
    ).to.have.property( 'isValid', true );
  } );

  it( 'should still work when presented with only a end date', function() {
    expect(
      dateRange.format( '', dateEnd )
    ).to.have.property( 'isValid', true );
  } );

  it( 'should still work when dates are flipped', function() {
    expect(
      dateRange.format( dateEnd, dateStart )
    ).to.have.property( 'isValid', true );
  } );
} );
