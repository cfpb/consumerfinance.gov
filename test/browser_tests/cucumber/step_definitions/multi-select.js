'use strict';


var BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

var SublandingFilterablePage = require( '../../page_objects/sublanding-filterable-page.js' );
var sublandingFilterablePage = new SublandingFilterablePage();

var {defineSupportCode} = require('cucumber');
var {expect} = require('chai');

defineSupportCode( function( { Then, When } ) {
  When('I expand the filter', function( ) {
    return sublandingFilterablePage.mExpandable.click();
  });

  Then ('I should be able to select topics using the multi-select', function( callback ) {
    sublandingFilterablePage.multiSelectSearch.click();
    browser.pause();
  });
});
