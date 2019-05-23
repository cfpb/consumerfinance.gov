const pagination = require( '../../shared_objects/pagination.js' );
const { When } = require( 'cucumber' );
const chai = require( 'chai' );
const chaiAsPromised = require( 'chai-as-promised' );

chai.use( chaiAsPromised );

When( /I click on the (.*) button(?:\s)?(?:again)?/,
  function( navigationButton ) {

    return pagination[navigationButton + 'Btn'].click();
  }
);

When( /I enter "(\d)" in the page input field/,
  function( pageNumber ) {

    return pagination.pageInput.sendKeys( pageNumber );
  }
);
