import { DelinquentMortgage } from '../../pages/data-research/deliquent-mortgages';
import { PrepaidAgreementsSearch } from '../../pages/data-research/prepaid-agreements-search';

const delinquentMortgage = new DelinquentMortgage();
const prepaidAgreementsSearch = new PrepaidAgreementsSearch();

describe( 'Data Research', () => {

  describe( 'Delinquent Mortgages', () => {

    it( 'should display delinquency trends chart for a given state', () => {
      delinquentMortgage.open();
      delinquentMortgage.selectLocationType( 'State' );
      delinquentMortgage.selectStateForDelinquencyTrends( 'Virginia' );
    } );

    it( 'should display delinquency rates by month for a given state', () => {
      delinquentMortgage.open();
      delinquentMortgage.selectStateForDelinquencyRatesPerMonth( 'Virginia' );
      delinquentMortgage.selectMonth( 'January' );
      delinquentMortgage.selectYear( '2017' );
      delinquentMortgage.mapTitle().should( 'contain', 'Virginia' );
      delinquentMortgage.mapTitle().should( 'contain', 'January' );
      delinquentMortgage.mapTitle().should( 'contain', '2017' );
    } );

  } );

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

} );
