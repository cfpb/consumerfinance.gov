export class AskCfpbSearch {

  open() {
    cy.visit( '/ask-cfpb/search/' );
  }

  search( term ) {
    cy.get( '#o-search-bar_query' ).type( term );
    cy.get( 'form[action="/ask-cfpb/search/"]' ).first().within( () => {
      cy.get( '.a-btn' ).click();
    } );
  }

  resultsSection() {
    return cy.get( '.search-results' );
  }

}
