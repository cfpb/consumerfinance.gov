
'use strict';

let BasePage = require( './wagtail-admin-base-page.js' );

class SublandingFilterablePage extends BasePage {

  constructor() {
    super();
    this.results = element.all( by.css( '.o-post-preview_content' ) );
	this.first_result = this.results.first();
	this.last_result = this.results.last();
	this.multiselect = element.all( by.css( '.cf-multi-select' ) );
    this.URL = '/sfp';
  }

}


module.exports = SublandingFilterablePage;