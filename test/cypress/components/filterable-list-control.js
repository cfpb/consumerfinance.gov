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

  openFilterableListControl() {
    return cy.get( '#o-filterable-list-controls' ).find( 'button' ).first().click();
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

  expandable() {
    return cy.get( '.o-filterable-list-controls .o-expandable' );
  }

  notification() {
    return cy.get( '.o-filterable-list_notification' );
  }

  open() {
    return this.openFilterableListControl();
  }

  applyFilters() {
    return cy.get( 'form[action="."]' ).submit();
  }

  clearFilters() {
    cy.get( '.a-btn__warning' ).click( { force: true } );
  }

  showFilters() {
    return cy.get( '[data-qa-hook="expandable"]' ).find( 'button' ).first().click();
  }

  hideFilters() {
    return cy.get( '[data-qa-hook="expandable"]' ).find( 'button' ).last().click();
  }

}
