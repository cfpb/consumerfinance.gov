export class PayingForCollege {

  openLoan() {
    cy.visit( '/paying-for-college/choose-a-student-loan/' );
  }

  openMoney() {
    cy.visit( '/paying-for-college/manage-your-college-money/' );
  }

  clickExpandable( name ) {
    cy.get( 'span' ).contains( name ).click();
  }

  clickBubble( name ) {
    cy.get( '.bubble-top-text' ).contains( name ).click();
  }

  closeAllBubbles() {
    cy.get( '.bubble-space .btn-close' ).each( el => {
      cy.wrap( el ).click( { force: true } );
    } );
  }

  closeFirstBubble() {
    cy.get( '.bubble-space .btn-close' ).first().click();
  }

  closeLastBubble() {
    cy.get( '.bubble-space .btn-close' ).last().click();
  }

}
