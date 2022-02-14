export class AskCfpbAnswerPage {

  open() {
    cy.visit( '/ask-cfpb/how-can-i-tell-if-a-friend-neighbor-or-family-member-is-a-victim-of-financial-exploitation/' );
  }

  clickSummary() {
    cy.get( '.o-summary_btn' ).click();
  }
}
