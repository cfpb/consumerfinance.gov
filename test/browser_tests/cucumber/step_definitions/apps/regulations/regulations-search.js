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

When( 'I filter by regulation {int}',
  reg => element( by.css( `label[for="regulation-${ reg }"]` ) ).click()
);

When( 'I wait for the search results to load',
  () => browser.wait(
    () => element( by.css( '#regs3k-results.is-loading' ) ).isPresent().then(
      present => !present
    ), 10000, 'The search results request timed out'
  )
);

Then( 'regulation {int} filter tag should appear',
  reg => element( by.css( `.a-tag[value="${ reg }"]` ) ).isPresent().then(
    present => expect( present ).to.be.true
  )
);
