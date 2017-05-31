'use strict';

var SublandingFilterablePage = require(
  '../../page_objects/sublanding-filterable-page.js'
);
var sublandingFilterablePage = new SublandingFilterablePage();
var { defineSupportCode } = require( 'cucumber' );
var { expect } = require( 'chai' );

defineSupportCode( function( { Then, When } ) {

  When( 'I goto a sublanding filterable page and do not select a filter',
    function() {
      sublandingFilterablePage.gotoURL();
    }
  );

  Then( 'I should see the first result', function() {

    return sublandingFilterablePage.first_result
           .getText()
           .then( function( first ) {
             expect( first ).to.contain( 'sfp child 0' );
           } );
  } );

  Then( 'I should see the last result', function() {

    return sublandingFilterablePage.last_result.getText( )
          .then( function( last ) {
            expect( last ).to.contain( 'sfp child 9' );
          } );
  } );

  Then( 'I should see the right number of results', function() {

    return sublandingFilterablePage.results.count( )
           .then( function( num ) {
             expect( num ).to.equal( 10 );
           } );
  } );

} );
