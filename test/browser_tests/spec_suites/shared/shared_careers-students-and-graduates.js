'use strict';

var StudentsAndGraduates = require(
    '../../page_objects/page_careers-students-and-graduates.js'
  );

describe( 'Careers/Student-and-graduates', function() {
  var page;

  beforeEach( function() {
    page = new StudentsAndGraduates();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toBe( 'Students and Graduates' );
  } );

  it( 'should have 4 opportunities for students and graduates', function() {
    expect( page.opportunities.count() ).toEqual( 4 );
    expect( page.opportunities.getText() )
      .toContain( 'Presidential Management Fellow' );
  } );

} );
