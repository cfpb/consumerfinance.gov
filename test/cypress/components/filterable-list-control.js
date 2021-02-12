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

  filterFromDate( date ) {
    return this.filterableListElement( 'from-date' ).type( date );
  }

  filterToDate( date ) {
    return this.filterableListElement( 'to-date' ).type( date );
  }

  results() {
    return cy.get( '.o-post-preview_content' );
  }

  firstResult() {
    return this.results().first();
  }

  lastResult() {
    return this.results().last();
  }

  notification() {
    return cy.get( '.o-filterable-list_notification' );
  }

  open() {
    return this.showFilters();
  }

  applyFilters() {
    return cy.get( 'form[action="."]' ).submit();
  }

  clearFilters() {
    cy.get( '.a-btn__warning' ).click( { force: true } );
  }

  showFilters() {
    return cy.get( '.o-expandable_cue-open' ).click( { force: true } );
  }

  hideFilters() {
    return cy.get( '.o-expandable_cue-close' ).click();
  }

}
