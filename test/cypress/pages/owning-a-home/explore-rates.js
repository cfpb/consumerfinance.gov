export class ExploreRates {

  open() {
    cy.visit( '/owning-a-home/explore-rates/' );
  }

  selectState( state ) {
    cy.get( '#location' )
      .select( state );
  }

  graph() {
    return cy.get( '#chart-section' )
      .within( () => cy.get( 'figure:first' ) );
  }

}
