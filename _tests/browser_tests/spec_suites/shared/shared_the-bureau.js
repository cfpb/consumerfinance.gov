var careers_studentsAndGraduates = require( '../../page_objects/page_the-bureau.js' );

describe( 'Beta Careers/Students and Graduates Page', function() {
  var page;

  beforeEach( function() {
    page = new TheBureauPage();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toBe( 'Students and Graduates' );
  } );

  it( 'should include 3 bureau missions, Educate, Enforce, Empower', function() {
    expect( page.missions.count() ).toEqual( 3 );
    expect( page.missions.getText() ).toEqual[ 'Educate', 'Enforce', 'Empower' ];
  } );
} );
