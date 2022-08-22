export class AskCfpbAnswerPage {

  open() {
    cy.visit( '/ask-cfpb/' ).get(
      '.ask-categories article li a'
    ).first().click();
  }

  clickSummary() {
    cy.get( '.o-summary_btn' ).click();
  }
}
