const util = require( '../../util/index.js' );
const shouldShouldnt = util.shouldShouldnt;

const { defineSupportCode } = require( 'cucumber' );
const { expect } = require( 'chai' );


defineSupportCode( function( { When, Then } ) {

  When( 'there exists a reusable text snippet on this page',
    function() {
      const rts = element( by.css( '.m-reusable-text-snippet' ) );
      return expect( rts.isPresent() ).to.eventually.equal( true );
    }
  );

  Then( /the snippet output (should|shouldn't) include a slug-style header/,
    function( includeHeader ) {
      let rts;

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
