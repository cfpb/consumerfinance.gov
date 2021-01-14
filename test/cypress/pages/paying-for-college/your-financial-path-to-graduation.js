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
    // Intercept calls to the schools API so results are immediately returned.
    cy.intercept( '/paying-for-college2/understanding-your-financial-aid-offer/api/search-schools.json?q=Harvard%20University', { fixture: 'search-schools' } ).as( 'searchSchools' );
    cy.intercept( '/paying-for-college2/understanding-your-financial-aid-offer/api/school/166027/', { fixture: 'harvard-university' } ).as( 'harvardUniversity' );

    cy.get( '#search__school-input' )
      .should( 'have.value', name ).then( searchInput => {
        cy.contains( '#search-results button', name ).then( btn => {
          if ( Cypress.dom.isAttached( btn ) ) {
            btn.click();
            cy.wait( '@harvardUniversity', 1000 ).then( interception => {
              cy.get( '#search-results' ).should( 'not.be.visible' );
            } );
          } else {
            throw new Error(
              'Button is not attached to the dom. ' +
              'This likely means the search box results markup was ' +
              'overwritten before the test completed.'
            );
          }
        } );
      } );
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
