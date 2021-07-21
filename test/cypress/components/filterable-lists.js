export class FilterableList {

  showFilters() {
    cy.get( '#o-filterable-list-controls' ).find( 'button' ).first().click();
  }

  filterForm() {
    return cy.get( '#o-filterable-list-controls form[action="."]' );
  }

  applyFilters() {
    cy.get( '#o-filterable-list-controls button[type="submit"]' ).click();
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

  openTopics() {
    cy.get( '#o-filterable-list-controls_topics' ).click();
  }

  selectTopic( topic ) {
    const id = topic.split( ' ' ).join( '-' ).toLowerCase();
    cy.get( `#topics-${ id }` ).check( { force: true } );
  }

  selectedTopics() {
    return cy.get( '.o-multiselect_choices > li' );
  }

}
