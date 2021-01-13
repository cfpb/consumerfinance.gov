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
    cy.get( '#search__school-input' ).type( name );
  }

  searchResults() {
    return cy.get( '#search-results' );
  }

  clickSearchResult( name ) {
    cy.get( '#search-results' ).contains( name ).click();
  }

  setText( name, value ) {
    cy.get( `#${ name }` ).clear().type( value );
  }

  selectProgram( program, name ) {
    cy.get( `#program-${ program }-radio_${ name } + label` ).click();
  }

  affordLoanChoice( name ) {
    cy.get( `#affording-loans-choices_${ name }` ).check( { force: true } );
  }

  actionPlan( name ) {
    cy.get( `#action-plan_${ name }` ).check( { force: true } );
  }
}
