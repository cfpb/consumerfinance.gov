export class PfcRepayStudentDebt {

  open() {
    cy.visit( '/paying-for-college/repay-student-debt/' );
  }

  selectQuestion( id, question ) {
    return cy.get( `#q${ id }` ).contains( question );
  }

  click( name ) {
    cy.get( '.btn' ).contains( name ).click( { force: true } );
  }

  clickResponse( id, name ) {
    cy.get( `#q${ id }` ).contains( name ).click( { force: true } );
  }
}
