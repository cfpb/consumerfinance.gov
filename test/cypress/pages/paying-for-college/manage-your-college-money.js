export class PfcManageCollegeMoney {

  openOption( name ) {
    cy.visit( `/paying-for-college/manage-your-college-money/#${ name }` );
  }

  expandOption( name ) {
    cy.get( 'span' ).contains( name ).click();
  }

  selectOption( name ) {
    cy.get( '.bubble-top-text' ).contains( name ).click();
  }

  closeOption( name ) {
    cy.get( '.bubble-transparent-answer' ).find( 'p' ).contains( name ).click( { force: true } );
  }

  closeFirstOption() {
    cy.get( '.btn-close' ).first().click( { force: true } );
  }

  closeLastOption() {
    cy.get( '.btn-close' ).last().click( { force: true } );
  }

}
