export class CreditCardAgreementSearch {

  open() {
    cy.visit( '/credit-cards/agreements/' );
  }

  getIssuer() {
    return cy.get( '#issuer_select' ).children().first().siblings().first();
  }

  selectIssuer( issuer ) {
    cy.get( '#issuer_select' ).select( issuer, { force: true } );
  }

  agreementsList() {
    return cy.get( '#ccagrsearch' );
  }

}
