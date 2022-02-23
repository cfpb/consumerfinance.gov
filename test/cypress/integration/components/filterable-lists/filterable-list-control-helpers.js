export class FilterableListControl {

  filterableListControl() {
    return cy.get( '.o-filterable-list-controls' );
  }

  filterableElement( selector ) {
    return this.filterableListControl().get( selector );
  }

  filterableListElement( name ) {
    return cy.get( `#o-filterable-list-controls_${ name }` );
  }

  filterItemName( name ) {
    return this.filterableListElement( 'title' ).type( name );
  }

  resultDate() {
    return cy.get( '.datetime_date:first' )
  }

  filterFromDate( date ) {
    return this.filterableListElement( 'from-date' ).type( date );
  }

  filterToDate( date ) {
    return this.filterableListElement( 'to-date' ).type( date );
  }

  resultsContent() {
    return cy.get( '.o-filterable-list_results .o-post-preview_content' );
  }

  firstResultContent() {
    return this.resultsContent().first();
  }

  resultTitle() {
    return cy.get( '.o-post-preview_title:first' );
  }

  lastResultContent() {
    return this.resultsContent().last();
  }

  resultsHeader( name ) {
    return cy.get( `.o-post-preview .m-meta-header_${ name }` );
  }

  resultsHeaderLeft() {
    return this.resultsHeader( 'left' );
  }

  resultsHeaderRight() {
    return this.resultsHeader( 'right' );
  }

  firstResultHeader() {
    return this.resultsHeaderRight().first();
  }

  lastResultHeader() {
    return this.resultsHeaderRight().last();
  }

  notification() {
    return cy.get( '.o-filterable-list_notification' );
  }

  open() {
    return this.showFilters();
  }

  applyFilters() {
    return cy.get( '#o-filterable-list-controls button[type="submit"]' ).click();
  }

  clearFilters() {
    cy.get( '.a-btn__warning' ).click( { force: true } );
  }

  showFilters() {
    return cy.get( '.o-filterable-list .o-expandable_cue-open' ).click();
  }

  hideFilters() {
    return cy.get( '.o-expandable_cue-close' ).click();
  }

}
