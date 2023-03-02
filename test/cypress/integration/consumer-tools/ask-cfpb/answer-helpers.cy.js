export class AskCfpbAnswerPage {
  open() {
    cy.visit('/ask-cfpb/').get('.ask-categories article li a').first().click();
  }

  getFirstLinkInSummary() {
    return cy.get('.o-summary_content a').first();
  }

  getSummaryBtn() {
    return cy.get('.o-summary_btn');
  }
}
