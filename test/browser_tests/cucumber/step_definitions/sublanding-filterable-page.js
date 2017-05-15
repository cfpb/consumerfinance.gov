'use strict';


var BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

var SublandingFilterablePage = require( '../../page_objects/sublanding-filterable-page.js' );
var sfp = new SublandingFilterablePage();

var {defineSupportCode} = require('cucumber');
var {expect} = require('chai');

defineSupportCode( function( {Then, When } ) {
	When( 'I goto a sublanding filterable page and do not select a filter', function() {
    	sfp.gotoURL();
  	});

  	Then ('I should see the first result', function() {
    	return sfp.first_result.getText().then( function(first) {
  			expect(first).to.contain('sfp child 0')
  		})
  	});

  	Then ('I should see the last result', function() {
  		return sfp.last_result.getText().then( function(last) {
  			expect(last).to.contain('sfp child 9')
  		})
  	});

  	Then ('I should see the right number of results', function() {
  		return sfp.results.count().then( function(num) {
  			expect(num).to.equal(10)
  		})
  	})

});