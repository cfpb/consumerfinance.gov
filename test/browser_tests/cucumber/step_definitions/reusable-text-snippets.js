const util = require( '../../util/index.js' );
const isShould = util.isShould;

const { When, Then } = require( 'cucumber' );
const { expect } = require( 'chai' );

When( 'there exists a reusable text snippet on this page',
  async function() {
    const rts = await element( by.css( '.m-reusable-text-snippet' ) );

    return expect( rts.isPresent() ).to.eventually.equal( true );
  }
);

Then( /the snippet output (should|shouldn't) include a slug-style header/,
  async function( includeHeader ) {
    let rts;

    if ( isShould( includeHeader ) ) {
      rts = await element.all( by.css( '.m-reusable-text-snippet' ) ).first();
    } else {
      rts = await element.all( by.css( '.m-reusable-text-snippet' ) ).last();
    }

    return expect( rts.element( by.css( '.m-slug-header' ) )
      .isPresent() )
      .to.eventually.equal( isShould( includeHeader ) );
  }
);
