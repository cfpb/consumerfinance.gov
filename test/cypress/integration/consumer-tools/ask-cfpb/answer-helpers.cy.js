export class AskCfpbAnswerPage {
  open() {
    cy.visit(
      '/ask-cfpb/if-i-pay-off-my-credit-card-balance-when-it-is-due-is-the-company-allowed-to-charge-me-interest-for-that-month-en-48/',
    );
  }

  getFirstLinkInSummary() {
    return cy.get('.o-summary__content a').first();
  }

  getSummaryBtn() {
    return cy.get('.o-summary__btn');
  }
}
