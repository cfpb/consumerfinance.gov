import {
  ConsumerComplaints
} from '../../../pages/data-research/consumer-complaints';

const page = new ConsumerComplaints();
const states = [
  'AK', 'AL', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID',
  'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS',
  'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR',
  'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
];

describe( 'Consumer Complaint Database', () => {
  beforeEach( () => {
    cy.visit( '/data-research/consumer-complaints/' );
  } );

  it( 'should display chart with complaints for all 50 states', () => {
    page.clickButton( 'Complaints' );
    page.checkLegend( 'description' ).should( 'contain', 'Complaints' );
    cy.get( '.cfpb-chart' ).should( 'be.visible' );
    states.forEach( name => {
      page.checkChart( name ).should( 'be.visible' );
    } );
    page.clickButton( 'Complaints per 1,000' );
    page.checkLegend( 'description' )
      .should( 'contain', 'Complaints per 1,000' );
    page.checkLegend( 'dates' ).should( 'be.visible' );
    states.forEach( name => {
      page.checkState( name ).should( 'be.visible' );
    } );
    page.clickTile( 'DC' );
    cy.url().should( 'include', 'state=DC' );
  } );

  it( 'should limit results by a date range', () => {
    page.click( 'View complaint data' );
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
    page.click( 'View complaint data' );
    page.clickTab( 'trends' );
    cy.url().should( 'include', 'tab=Trends' );
    page.enter( 'money' );
    page.search();
    page.searchSummary().should( 'be.visible' );
    cy.url().should( 'include', 'searchField' );
  } );

  it( 'should search based on multiple terms', () => {
    page.click( 'View complaint data' );
    page.clickTab( 'list' );
    cy.url().should( 'include', 'tab=List' );
    page.enter( 'loan sold' );
    page.search();
    page.searchSummary().should( 'be.visible' );
    cy.url().should( 'include', 'searchText=loan' );
  } );

  it( 'should display Download the data', () => {
    page.click( 'Download options and API' );
    cy.url().should( 'include', 'download-the-data' );
  } );

  it( 'should display Consumer Response annual report', () => {
    page.click( 'Read our annual report' );
    cy.url().should( 'include', 'consumer-response-annual-report' );
  } );

} );
