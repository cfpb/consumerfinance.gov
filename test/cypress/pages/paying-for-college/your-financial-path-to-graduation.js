export class PfcFinancialPathToGraduation {

  click( name ) {
    cy.get( '.a-btn' ).contains( name ).click();
  }

  clickGetStarted() {
    cy.get( '.btn__get-started' ).click();
  }

  clickNextStep() {
    cy.get( '.btn__next-step' ).click();
  }

  enter( name ) {
    cy.get( '#search__school-input' ).type( name, { force: true } );
  }

  searchResults() {
    return cy.get( '#search-results' );
  }

  setText( name, value ) {
    cy.get( `#${ name }` ).type( value );
  }

  selectProgram( program, name ) {
    cy.get( `#program-${ program }-radio_${ name }` ).check( { force: true } );
  }

  affordLoanChoice( name ) {
    cy.get( `#affording-loans-choices_${ name }` ).check( { force: true } );
  }

  actionPlan( name ) {
    cy.get( `#action-plan_${ name }` ).check( { force: true } );
  }
}
