export class FilterableListControl {
  filterableListControl() {
    return cy.get('.o-filterable-list-controls');
  }

  filterableElement(selector) {
    return this.filterableListControl().get(selector);
  }

  filterableListElement(name) {
    return cy.get(`#o-filterable-list-controls_${name}`);
  }

  filterItemName(name) {
    return this.filterableListElement('title').type(name);
  }

  resultDate() {
    return cy.get('.datetime time:first');
  }

  filterFromDate(date) {
    return this.filterableListElement('from-date').type(date);
  }

  filterToDate(date) {
    return this.filterableListElement('to-date').type(date);
  }

  getResults() {
    return cy.get('[data-cy=filterable-list-results]');
  }

  getResultCategoryHasTags() {
    return this.getResults()
      .find('.a-tag-topic')
      .closest('.o-post-preview')
      .find('.m-meta-header__item:first');
  }

  getResultTagHasCategories() {
    return this.getResults()
      .find('.m-meta-header__item:first')
      .closest('.o-post-preview')
      .find('.a-tag-topic:first');
  }

  getResultTag() {
    return this.getResults().find('.a-tag-topic:first');
  }

  getResultTitleHasTag() {
    return this.getResults()
      .find('.a-tag-topic:first')
      .closest('.o-post-preview')
      .find('.o-post-preview__title:first');
  }

  getResultCategory() {
    return this.getResults().find('.m-meta-header__item:first');
  }

  getResultTitleHasCategory() {
    return this.getResults()
      .find('.m-meta-header__item:first')
      .closest('.o-post-preview')
      .find('.o-post-preview__title:first');
  }

  resultsHeaderContent() {
    return this.getResults().find('.m-meta-header');
  }

  resultsContent() {
    return this.getResults().find('.o-post-preview__content');
  }

  firstResultContent() {
    return this.resultsContent().first();
  }

  resultTitle() {
    return cy.get('.o-post-preview__title:first');
  }

  lastResultContent() {
    return this.resultsContent().last();
  }

  resultsHeaderLeft() {
    return cy.get(
      `.o-post-preview .m-meta-header__item-group .m-meta-header__item:first`,
    );
  }

  resultsHeaderRight() {
    return cy.get(`.o-post-preview .m-meta-header__item`);
  }

  firstResultHeader() {
    return this.resultsHeaderRight().first();
  }

  lastResultHeader() {
    return this.resultsHeaderRight().last();
  }

  notification() {
    return cy.get('[data-cy=filterable-list-notification]');
  }

  open() {
    return this.showFilters();
  }

  applyFilters() {
    return cy.get('#o-filterable-list-controls button[type="submit"]').click();
  }

  clearFilters() {
    cy.get('.a-btn--warning').click({ force: true });
  }

  showFilters() {
    return cy.get('.o-filterable-list .o-expandable__cue-open').click();
  }

  hideFilters() {
    return cy.get('.o-expandable__cue-close').click();
  }
}
