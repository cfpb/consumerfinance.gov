export class ObtenerRespuestasBuscar {

  open() {
    cy.visit( '/es/obtener-respuestas/' );
  }

  enter( term ) {
    cy.get( '#o-search-bar_query' ).type( term );
  }

  autocomplete() {
    return cy.get( '.m-autocomplete_results' );
  }

  search() {
    cy.get( 'form[action="/es/obtener-respuestas/buscar/"]' ).first().within( () => {
      cy.get( '.a-btn' ).click();
    } );
  }

  resultsSection() {
    return cy.get( '.search-results' );
  }

  resultsHeader() {
    return cy.get( '.results-header' );
  }
}
