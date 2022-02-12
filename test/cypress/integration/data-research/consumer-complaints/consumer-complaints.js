/* import { ConsumerComplaints } from './consumer-complaints-helpers';

const page = new ConsumerComplaints();

describe( 'Consumer Complaint Database', () => {
  beforeEach( () => {
    cy.visit( '/data-research/consumer-complaints/' );
  } );

  it( 'should limit results by a date range', () => {
    page.click( 'Explore data and trends' );
    page.clickDateRange( '3m' );
    cy.url().should( 'include', 'dateRange=3m' );
    page.clickDateRange( '6m' );
    cy.url().should( 'include', 'dateRange=6m' );
    page.clickDateRange( '1y' );
    cy.url().should( 'include', 'dateRange=1y' );
    page.clickDateRange( '3y' );
    cy.url().should( 'include', 'dateRange=3y' );
    page.clickDateRange( 'All' );
    cy.url().should( 'include', 'dateRange=All' );
  } );

  it( 'should limit results by search query', () => {
    page.click( 'Read complaints' );
    page.clickTab( 'trends' );
    cy.url().should( 'include', 'tab=Trends' );
    page.enter( 'money' );
    page.search();
    page.searchSummary().should( 'be.visible' );
    cy.url().should( 'include', 'searchField' );
  } );

  it( 'should search based on multiple terms', () => {
    page.click( 'Explore data and trends' );
    page.clickTab( 'list' );
    cy.url().should( 'include', 'tab=List' );
    page.enter( 'loan sold' );
    page.search();
    page.searchSummary().should( 'be.visible' );
    cy.url().should( 'include', 'searchText=loan' );
  } );

  it( 'should display Download the data', () => {
    page.click( 'Download complaint data' );
    cy.url().should( 'include', 'download-the-data' );
  } );

} ); */
