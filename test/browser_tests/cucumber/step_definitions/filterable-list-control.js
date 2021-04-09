const filterableListControl = require(
  '../../shared_objects/filterable-list-control.js'
);
const { When } = require( '@cucumber/cucumber' );

When( /I (.*) the filterable list control/, function( action ) {

  return filterableListControl[action]();
} );
