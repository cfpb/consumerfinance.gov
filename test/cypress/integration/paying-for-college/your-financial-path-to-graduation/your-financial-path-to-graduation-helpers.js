export class PfcFinancialPathToGraduation {

  clickGetStarted() {
    cy.get( '.btn__get-started' ).click();
  }

  clickNextStep() {
    cy.get( '.btn__next-step' ).click();
  }

  enter( name ) {
    // Intercept calls to the schools API so results are immediately returned.
    cy.intercept( '/paying-for-college2/understanding-your-financial-aid-offer/api/search-schools.json?q=Harvard%20University', { fixture: 'search-schools' } ).as( 'searchSchools' );

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
    // Intercept calls to the schools API so results are immediately returned.
    cy.intercept( '/paying-for-college2/understanding-your-financial-aid-offer/api/school/166027/', { fixture: 'harvard-university' } ).as( 'harvardUniversity' );

    cy.contains( '#search-results button', name ).click();
    cy.wait( '@harvardUniversity' );
    cy.get( '#search-results' ).should( 'not.be.visible' );
  }

  typeText( name, value ) {
    cy.get( `#${ name }` ).type( value );
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
