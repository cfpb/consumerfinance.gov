export class AskCfpbAnswerPage {
  open() {
    cy.visit(
      '/ask-cfpb/what-effect-will-shopping-for-an-auto-loan-have-on-my-credit-en-15/',
    );
  }

  getFirstLinkInSummary() {
    return cy.get('.o-summary__content a').first();
  }

  getSummaryBtn() {
    return cy.get('.o-summary__btn');
  }
}
