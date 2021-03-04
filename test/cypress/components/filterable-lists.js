export class FilterableList {

  open() {
    cy.visit( '/data-research/research-reports/' );
  }

  showFilters() {
    cy.get( '#o-filterable-list-controls' ).find( 'button' ).first().click();
  }

  filterForm() {
    return cy.get( 'form[action="."]' );
  }

  selectFilter( category ) {
    const id = `#filter_categories_${ category.split( ' ' ).join( '-' ) }`.toLowerCase();
    cy.get( id ).check( { force: true } );
  }

  applyFilters() {
    this.filterForm().submit();
  }

  filterNotification() {
    return cy.get( '.o-filterable-list_notification' );
  }

  clearFilters() {
    cy.get( '.a-btn__warning' ).click();
  }

  setFromDate( date ) {
    cy.get( '#o-filterable-list-controls_from-date' ).type( date );
  }

  setToDate( date ) {
    cy.get( '#o-filterable-list-controls_to-date' ).type( date );
  }

  selectTopic( topic ) {
    const id = topic.split( ' ' ).join( '-' ).toLowerCase();
    cy.get( `#topics-${ id }` ).check( { force: true } );
  }

  selectedTopics() {
    return cy.get( '.o-multiselect_choices > li' );
  }

}
