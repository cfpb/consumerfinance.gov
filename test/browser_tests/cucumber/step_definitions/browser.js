const { When } = require( '@cucumber/cucumber' );
const chai = require( 'chai' );
const chaiAsPromised = require( 'chai-as-promised' );

chai.use( chaiAsPromised );

When( 'I wait {int} seconds',
  seconds => browser.sleep( seconds * 1000 )
);
