export class AskCfpbAnswerPage {
  open() {
    cy.visit('/ask-cfpb/').get('.ask-categories article li a').first().click();
  }

  getSummaryContentLink() {
    return cy.get('a').contains('how to keep your credit score(s) up');
  }

  getSummaryBtn() {
    return cy.get('.o-summary_btn');
  }

  clickSummary() {
    cy.get('.o-summary_btn').click();
  }
}
