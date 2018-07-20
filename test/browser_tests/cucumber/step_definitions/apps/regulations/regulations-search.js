const { Then, When } = require( 'cucumber' );
const chai = require( 'chai' );
const expect = chai.expect;
const chaiAsPromised = require( 'chai-as-promised' );

chai.use( chaiAsPromised );

When( 'I enter {string} in the regulations search field',
  searchTerm => element( by.css( '#query' ) ).sendKeys( searchTerm )
);

When( 'I submit the search form',
  () => element( by.css( '.search_form button' ) ).click()
);
