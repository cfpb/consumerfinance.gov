export class ConsumerComplaints {

  click( name ) {
    cy.get( '.m-list_link' ).contains( name ).click();
  }

  clickTab( name ) {
    cy.get( `.${ name }` ).click();
  }

  clickDateRange( name ) {
    cy.get( `.range-${ name }` ).click();
  }

  clickButton( name ) {
    cy.get( '.a-btn' ).contains( name ).click();
  }

  enter( term ) {
    cy.get( '#searchText.a-text-input' ).type( term );
  }

  search() {
    cy.get( '.a-btn.flex-fixed' ).click();
  }

  searchSummary() {
    return cy.get( '#search-summary' );
  }

}
