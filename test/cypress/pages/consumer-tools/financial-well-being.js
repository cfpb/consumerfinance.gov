export class FinancialWellBeing {
  open() {
    cy.visit( '/consumer-tools/financial-well-being/' );
  }

  selectQuestion( questionNumber, answer ) {
    const id = `#question_${ questionNumber }-${ answer.split( ' ' ).join( '-' ) }`.toLowerCase();
    cy.get( id ).check( { force: true } );
  }

  selectAge() {
    cy.get( '#age-18-61' ).check( { force: true } );
  }

  submitButton() {
    return cy.get( '#submit-quiz' );
  }

  submit() {
    this.submitButton().click();
  }

  score() {
    return cy.get( 'figure' );
  }

}
