'use strict';

const filterableListControl = require( '../shared_objects/filterable-list-control' );
const BaseFilteablePage = require( './base-filterable-page.js' );

class BrowseFilterablePage extends BaseFilteablePage {

  constructor() {
    super();
    this.URL = '/bfp';
  }
}

module.exports = BrowseFilterablePage;
