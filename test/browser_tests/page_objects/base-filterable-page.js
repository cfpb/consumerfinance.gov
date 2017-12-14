const BasePage = require( './base-page.js' );

class BaseFilterablePage extends BasePage {

  constructor() {
    super();
    this.results = element.all( by.css( '.o-post-preview_content' ) );
    this.firstResult = this.results.first();
    this.lastResult = this.results.last();
    this.multiselect = element.all( by.css( '.cf-multi-select' ) );
  }

  getResultsCount() {
    return this.results.count()
      .then( count => count.toString() );
  }

  getResultText( resultPosition = 'first' ) {
    return this[resultPosition + 'Result'].getText();
  }
}

module.exports = BaseFilterablePage;
