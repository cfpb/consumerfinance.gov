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
    return cy.get('.datetime_date:first');
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
      .find('.m-tags_tag')
      .closest('.o-post-preview')
      .find('.m-meta-header_item:first');
  }

  getResultTagHasCategories() {
    return this.getResults()
      .find('.m-meta-header_item:first')
      .closest('.o-post-preview')
      .find('.m-tags_tag:first');
  }

  getResultTag() {
    return this.getResults().find('.m-tags_tag:first');
  }

  getResultTitleHasTag() {
    return this.getResults()
      .find('.m-tags_tag:first')
      .closest('.o-post-preview')
      .find('.o-post-preview_title:first');
  }

  getResultCategory() {
    return this.getResults().find('.m-meta-header_item:first');
  }

  getResultTitleHasCategory() {
    return this.getResults()
      .find('.m-meta-header_item:first')
      .closest('.o-post-preview')
      .find('.o-post-preview_title:first');
  }

  resultsHeaderContent() {
    return this.getResults().find('.m-meta-header');
  }

  resultsContent() {
    return this.getResults().find('.o-post-preview_content');
  }

  firstResultContent() {
    return this.resultsContent().first();
  }

  resultTitle() {
    return cy.get('.o-post-preview_title:first');
  }

  lastResultContent() {
    return this.resultsContent().last();
  }

  resultsHeaderLeft() {
    return cy.get(
      `.o-post-preview .m-meta-header_item-group .m-meta-header_item:first`,
    );
  }

  resultsHeaderRight() {
    return cy.get(`.o-post-preview .m-meta-header_item`);
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
    cy.get('.a-btn__warning').click({ force: true });
  }

  showFilters() {
    return cy.get('.o-filterable-list .o-expandable_cue-open').click();
  }

  hideFilters() {
    return cy.get('.o-expandable_cue-close').click();
  }
}
