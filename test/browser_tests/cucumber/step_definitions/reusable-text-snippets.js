'use strict';


var util = require( '../../util/index.js' );
var shouldShouldnt = util.shouldShouldnt;

var { defineSupportCode } = require( 'cucumber' );
var { expect } = require( 'chai' );


defineSupportCode( function( { When, Then } ) {

  When( 'there exists a reusable text snippet on this page',
    function() {
      var rts = element( by.css( '.m-reusable-text-snippet' ) );
      return expect( rts.isPresent() ).to.eventually.equal( true );
    }
  );

  Then( /the snippet output (should|shouldn't) include a slug-style header/,
    function( includeHeader ) {
      var rts;

      if ( shouldShouldnt( includeHeader ) ) {
        rts = element.all( by.css( '.m-reusable-text-snippet' ) ).first();
      } else {
        rts = element.all( by.css( '.m-reusable-text-snippet' ) ).last();
      }

      return expect( rts.element( by.css( '.m-slug-header' ) ).isPresent() )
             .to.eventually.equal( shouldShouldnt( includeHeader ) );
    }
  );

} );
