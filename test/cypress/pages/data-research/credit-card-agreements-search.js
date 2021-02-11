export class CreditCardAgreementSearch {

  open() {
    cy.visit( '/credit-cards/agreements/' );
  }

  selectIssuer( issuer ) {
    const element = issuer.split( ' ' ).join( '-' ).toLowerCase();
    cy.get( '#issuer_select' ).select( element, { force: true } );
  }

  agreementsList() {
    return cy.get( '#ccagrsearch' );
  }

}
