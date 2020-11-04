export class PfcRepayStudentDebt {

  open() {
    cy.visit( '/paying-for-college/repay-student-debt/' );
  }

  selectQuestion ( questionNumber ) {
    const id = `#q${ questionNumber }`
    return cy.get ( id );
  }

  click( name ) {
    cy.get( '.btn' ).contains( name ).click( { force: true } );
  }

}
