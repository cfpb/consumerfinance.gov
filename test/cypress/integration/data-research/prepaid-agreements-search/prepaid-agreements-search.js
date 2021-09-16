import { PrepaidAgreementsSearch } from './prepaid-agreements-search-helpers';

const prepaidAgreementsSearch = new PrepaidAgreementsSearch();

describe( 'Prepaid Agreements', () => {

  it( 'should search based on term', () => {
    prepaidAgreementsSearch.open();
    prepaidAgreementsSearch.searchByTerm( 'metro' );
    cy.url().should( 'include', 'q=metro' );
  } );

  it( 'should limit results when a search field is selected', () => {
    prepaidAgreementsSearch.open();
    prepaidAgreementsSearch.selectField( 'Product name' );
    prepaidAgreementsSearch.searchByTerm( 'Visa' );
    cy.url().should( 'include', '?search_field=name&q=Visa' );
  } );

  it( 'should limit results by issuer name when selected', () => {
    prepaidAgreementsSearch.open();
    prepaidAgreementsSearch.selectIssuer( 'Regions Bank' );
    prepaidAgreementsSearch.applyFilters();
    prepaidAgreementsSearch.filters().should( 'contain', 'Regions' );
  } );

  it( 'should filter by product type', () => {
    prepaidAgreementsSearch.open();
    prepaidAgreementsSearch.expandProductFilters();
    prepaidAgreementsSearch.selectProductType( 'Other' );
    prepaidAgreementsSearch.applyFilters();
    prepaidAgreementsSearch.filters().should( 'contain', 'Other' );
  } );

  it( 'should filter by current status', () => {
    prepaidAgreementsSearch.open();
    prepaidAgreementsSearch.expandCurrentStatusFilters();
    prepaidAgreementsSearch.selectStatus( 'Active' );
    prepaidAgreementsSearch.applyFilters();
    prepaidAgreementsSearch.filters().should( 'contain', 'Active' );
  } );

} );
