export class CreditCardAgreementSearch {
  open() {
    cy.visit('/credit-cards/agreements/');
  }

  openContainer() {
    return cy.get('#select-root').children().first().click();
  }

  agreementsList() {
    return cy.get('#react-select-2-listbox');
  }
}
