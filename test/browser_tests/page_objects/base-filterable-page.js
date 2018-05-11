const BasePage = require( './base-page.js' );

class BaseFilterablePage extends BasePage {

  async setElements() {
    this.results = await element.all( by.css( '.o-post-preview_content' ) );
    this.firstResult = this.results[0];
    this.lastResult = this.results[this.results.length - 1];
    this.multiselect = await element.all( by.css( '.cf-multi-select' ) );
  }

  getResultsCount() {
    const count = this.results.length;

    return count.toString();
  }

  getResultText( resultPosition = 'first' ) {
    return this[resultPosition + 'Result'].getText();
  }
}

module.exports = BaseFilterablePage;
