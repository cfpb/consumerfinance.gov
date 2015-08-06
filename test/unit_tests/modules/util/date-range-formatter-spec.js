'use strict';
var chai = require( 'chai' );
var sinon = require( 'sinon' );
var expect = chai.expect;
var jsdom = require( 'mocha-jsdom' );
var dateRange = require(
  '../../../../src/static/js/modules/util/date-range-formatter.js'
);

var test = {
  dateFormat: 'mm/dd/yyyy',
  dateStart: new Date( '01/01/2014' ),
  dateEnd: new Date( '12/31/2014' ),
  fakeDateStart: '01/01/2014',
  fakeDateEnd: '12/31/2014',
  notDate: 'foo'
}

describe( 'dateRangeFormatter', function() {
  it( 'should transform dates to yyyy-mm-dd format by default', function() {
    expect(
      dateRange.format( test.dateStart, test.dateEnd )
    ).to.have.property( 'startDate', '2014-01-01' );

    expect(
      dateRange.format( test.dateStart, test.dateEnd )
    ).to.have.property( 'isValid', true );
  } );

  it( 'should transform date-like strings to yyyy-mm-dd', function() {
    expect(
      dateRange.format( test.fakeDateStart, test.fakeDateEnd )
    ).to.have.property( 'startDate', '2014-01-01' );

    expect(
      dateRange.format( test.fakeDateStart, test.fakeDateEnd )
    ).to.have.property( 'isValid', true );
  } );

  it( 'isValid property should return false when presented with non-dates', function() {
    expect(
      dateRange.format( test.notDate, test.notDate )
    ).to.have.property( 'isValid', false );;
  } );

  it( 'should still work when presented with only a start date', function() {
    expect(
      dateRange.format( test.dateStart )
    ).to.have.property( 'isValid', true );
  });

  it( 'should still work when presented with only a end date', function() {
    expect(
      dateRange.format( '', test.dateEnd )
    ).to.have.property( 'isValid', true );
  });

  it( 'should still work when dates are flipped', function() {
    expect(
      dateRange.format( test.dateEnd, test.dateStart )
    ).to.have.property( 'isValid', true );
  });
} );
