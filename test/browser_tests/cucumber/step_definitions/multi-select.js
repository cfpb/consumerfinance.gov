'use strict';


var BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

var SublandingFilterablePage = require( '../../page_objects/sublanding-filterable-page.js' );
var sublandingFilterablePage = new SublandingFilterablePage();
const EC = protractor.ExpectedConditions;

var {defineSupportCode} = require('cucumber');
var {expect} = require('chai');

defineSupportCode( function( { Then, When } ) {
  When( 'I goto a filterable page', function() {
  	sublandingFilterablePage.gotoURL();
  });

  Then ('I should be able to select topics using the multi-select', function( ) {
    return sublandingFilterablePage.expandable.click().then( function ( ) {
    	return browser.wait( EC.elementToBeClickable( sublandingFilterablePage.multi_select_search) ).then( function ( ) {
			sublandingFilterablePage.multi_select_search.click();
		})
	 })
  });

});
