const FilterableBasePage = require( './base-filterable-page.js' );

class SublandingFilterablePage extends FilterableBasePage {

  constructor() {
    super();
    this.URL = '/sfp';
  }
}

module.exports = SublandingFilterablePage;
