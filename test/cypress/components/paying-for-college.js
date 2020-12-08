export class PayingForCollege {

  openLoanOption( name ) {
    cy.visit( `/paying-for-college/choose-a-student-loan/#${ name }` );
  }

  openMoneyOption( name ) {
    cy.visit( `/paying-for-college/manage-your-college-money/#${ name }` );
  }

  clickOption( name ) {
    cy.get( 'span' ).contains( name ).click();
  }

  selectOption( name ) {
    cy.get( '.bubble-top-text' ).contains( name ).click();
  }

  closeOption( name ) {
    cy.get( '.bubble-transparent-answer' ).find( 'p' ).contains( name ).click();
  }

  closeAllOptions() {
    cy.get( '.btn-close' ).each( el => {
      cy.wrap( el ).click( { force: true } );
    } );
  }

  closeFirstOption() {
    cy.get( '.btn-close' ).first().click();
  }

  closeLastOption() {
    cy.get( '.btn-close' ).last().click();
  }

}
