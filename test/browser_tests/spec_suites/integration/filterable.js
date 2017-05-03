'use strict';

var Blog = require( '../../page_objects/sublanding_filterable_page.js' );

describe( 'Browse filterable', function() {

  describe( 'pagination', function() {
    var page;

    beforeEach( function() {
      page = new Blog();
      page.get();
    } );


    xit ('should show the results when no filters are selected', function() {
      expect( page.results.getText() ).toContain('sfp child');
    } );



  } );
} );
