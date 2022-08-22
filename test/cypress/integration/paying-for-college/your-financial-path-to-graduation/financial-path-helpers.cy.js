export class PfcFinancialPathToGraduation {

  clickGetStarted() {
    cy.get( '.btn__get-started' ).click();
  }

  clickNextStep() {
    cy.get( '.btn__next-step' ).click();
  }

  enter( name ) {
    /* The following pastes the `name` value into the input and manually fires
       the keyup event. This is used so that the search-schools API is only
       called once, instead of each time a key is typed in. This prevents
       several API calls from occurring in the tests, which made them flaky.
    */
    cy.get( '#search__school-input' ).invoke( 'val', name ).trigger( 'keyup' );
  }

  searchResults() {
    return cy.get( '#search-results' );
  }

  clickSearchResult( name ) {

    cy.contains( '#search-results button', name ).click();
    cy.get( '#search-results' ).should( 'not.be.visible' );
  }

  typeText( name, value ) {
    cy.get( `#${ name }` ).type( value );
  }

  clickLeftNav( name ) {
    cy.get( `[data-nav_item="${ name }"]` ).click();
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

  costsQuestionChoice( name ) {
    cy.get( `label[for="costs-offer-radio_${ name }"]` ).click();
    cy.get( '#costs-offer-button' ).click();
  }
}
