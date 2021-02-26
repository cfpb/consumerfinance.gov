export class ActivitySearch {

  open() {
    cy.visit( '/consumer-tools/educator-tools/youth-financial-education/teach/activities/' );
  }

  selectFilter( label ) {
    cy.contains( label ).siblings( 'input' ).check( { force: true } );
  }

  clearFilters() {
    return cy.get( '.results_filters-clear' );
  }

  resultsFilterTag( filterName ) {
    return cy.get( `[data-value="#building-block--${ filterName }"]` );
  }

  resultsCountEmpty() {
    return cy.get( '.results_count__empty' );
  }

  search( term ) {
    cy.get( '#search-text' ).type( term );
    cy.get( 'form[action="."]' ).within( () => {
      cy.get( 'button' ).first().click();
    } );
  }

}
