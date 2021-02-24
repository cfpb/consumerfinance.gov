import { GlobalSearch } from '../../components/global-search';

const search = new GlobalSearch();

describe( 'Global Search molecule to search for content on the site', () => {
  before( () => {
    cy.visit( '/' );
  } );
  it( 'on page load', () => {
    // Then the search molecule should have a search trigger
    search.trigger().should( 'be.visible' );
    // And it shouldn't have search input content
    search.content().should( 'contain', '' );
    // And it shouldn't have suggested search terms
    search.suggest().should( 'contain', '' );
  } );
  it( 'after clicking search', () => {
    // When I click on the search molecule
    search.trigger().click( { force: true } );
    // Then the search molecule shouldn't have a search trigger
    search.trigger().should( 'not.be.visible' );
    // And it should have search input content
    search.content().should( 'be.visible' );
    // And it should focus the search input field
    search.input().should( 'have.focus' );
  } );
  it( 'after entering Text, should navigate to search portal', () => {
    // Then I click on the search molecule
    search.trigger().click( { force: true } );
    // When I enter "test" in the search molecule
    search.input().type( 'test' );
    // Then I should navigate to search portal
    /*  const portalUrl = 'https://search.consumerfinance.gov/' +
                          'search?utf8=%E2%9C%93&affiliate=cfpb&query=test';
        search.button().click( { force: true } );
        cy.url().should( 'include', portalUrl ); */
  } );
  it( 'after clicking off search', () => {
    // And I click off the search molecule
    search.footerTagline().click( { force: true } );
    // Then it shouldn't have search input content
    search.content().should( 'contain', '' );
  } );
  it( 'after the tab key is pressed', () => {
    // When I focus on the search molecule trigger
    search.trigger().type( ' ' );
    // And I perform tab actions on the search molecule
    /* search.input().type( '{tab}' ); */
    cy.tab();
    // Then it shouldn't have search input content
    search.content().should( 'contain', '' );
  } );
} );
