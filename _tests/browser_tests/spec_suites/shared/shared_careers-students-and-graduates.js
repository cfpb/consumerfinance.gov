var careers_studentsAndGraduates = require( '../../page_objects/page_careers-students-and-graduates.js' );

describe( 'Beta The Bureau Page', function() {
  var page;

  beforeEach( function() {
    page = new careers_studentsAndGraduates();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toBe( 'Students and Graduates' );
  } );

  it( 'should have 4 opportunities for students and graduates', function() {
    expect( page.opportunities.count() ).toEqual( 4 );
    expect( page.opportunities.getText() ).toInclude( 'Presidential Management Fellow' );
  } );
} );
