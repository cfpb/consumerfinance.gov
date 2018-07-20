const { Then } = require( 'cucumber' );
const chai = require( 'chai' );
const expect = chai.expect;
const chaiAsPromised = require( 'chai-as-promised' );

chai.use( chaiAsPromised );

Then( 'the page url should contain {string}',
  urlComponent => expect( browser.getCurrentUrl() )
    .to.eventually
    .contain( urlComponent )
);
