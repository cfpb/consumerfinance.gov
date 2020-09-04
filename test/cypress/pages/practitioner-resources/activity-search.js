export class ActivitySearch {

  open() {
    cy.visit( '/practitioner-resources/youth-financial-education/teach/activities' );
  }

  selectFilter( label ) {
    cy.contains( label ).siblings( 'input' ).check( { force: true } );
  }

  clearFilters() {
    return cy.get( '.results_filters-clear' );
  }

  search( term ) {
    cy.get( '#search-text' ).type( term );
    cy.get( 'form[action="."]' ).within( () => {
      cy.get( 'button' ).first().click();
    } );
  }

}
