export class PrepaidAgreementsSearch {

  open() {
    cy.visit( '/data-research/prepaid-accounts/search-agreements/' );
  }

  searchByTerm( term ) {
    cy.get( '#searchText' ).type( term );
    this.searchForm().submit();
  }

  searchForm() {
    return cy.get( '.search_wrapper' ).find( 'form' );
  }

  selectField( field ) {
    cy.get( '#search_field' ).select( field );
  }

  selectIssuer( issuer ) {
    cy.get( '#issuer_name' ).type( issuer );
    cy.get( `input[value="${ issuer }"]` ).check( { force: true } );
  }

  filtersForm() {
    return cy.get( '.content_sidebar' ).find( 'form' );
  }

  applyFilters() {
    this.filtersForm().submit();
  }

  filters() {
    return cy.get( '.filters_tags' );
  }

  expandProductFilters() {
    cy.get( 'span' ).contains( 'Prepaid product type' ).click();
  }

  selectProductType( product ) {
    this.filtersForm().find( `input[value="${ product }"]` ).check( { force: true } );
  }

  expandCurrentStatusFilters() {
    cy.get( 'span' ).contains( 'Current status' ).click();
  }

  selectStatus( status ) {
    this.filtersForm().find( `input[value="${ status }"]` ).check( { force: true } );
  }

}
