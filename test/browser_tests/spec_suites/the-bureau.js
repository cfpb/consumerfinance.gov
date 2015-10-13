'use strict';

var TheBureauPage = require( '../page_objects/page_the-bureau.js' );

describe( 'The Bureau Page', function() {
  var page;

  beforeAll( function() {
    page = new TheBureauPage();
    page.get();
  } );

  it( 'should properly load in a browser',
    function() {
      expect( page.pageTitle() ).toBe( 'The Bureau' );
    }
  );

  it( 'should have a hero',
    function() {
      expect( page.hero.isPresent() ).toBe( true );
    }
  );

  it( 'should have a video player',
    function() {
      expect( page.heroVideoPlayer.isPresent() ).toBe( true );
    }
  );

  it( 'should have a side nav',
    function() {
      expect( page.sideNav.isPresent() ).toBe( true );
    }
  );

  it( 'should include Bureau history',
    function() {
      expect( page.bureauHistory.isPresent() ).toBe( true );
    }
  );

  it( 'should include Bureau functions',
    function() {
      expect( page.bureauFunctions.isPresent() ).toBe( true );
    }
  );

  it( 'should include the Director’s Bio',
    function() {
      expect( page.directorsName.getText() ).toEqual( 'Richard Cordray' );
      expect( page.directorsBio.isPresent() ).toBe( true );
    }
  );

  it( 'should include the Deputy Director’s Bio',
    function() {
      expect( page.deputyDirectorsName.getText() ).toEqual( 'Meredith Fuchs' );
      expect( page.deputyDirectorsBio.isPresent() ).toBe( true );
    }
  );

  it( 'should include three Bureau mission statements',
    function() {
      expect( page.bureauMission.count() ).toEqual( 3 );
    }
  );

} );
