import { Pagination } from '../../components/pagination';

const page = new Pagination();

describe( 'Pagination molecule to navigate on the filterable pages', () => {
  beforeEach( () => {
    cy.visit( '/about-us/blog/' );
  } );
  it( 'Navigate to the next page', () => {
    // When I click on the next button
    page.clickNextButton();
    // Then the page url should contain "page=2"
    cy.url().should( 'include', 'page=2' );
  } );
  it( 'Navigate to the second page', () => {
    // When I enter "2" in the page input field
    page.enter( '2' );
    // And I click on the next button again
    page.clickNextButton();
    // Then the page url should contain "page=2"
    cy.url().should( 'include', 'page=2' );
  } );
  it( 'Navigate to the previous page', () => {
    // When I click on the next button
    page.clickNextButton();
    // And I click on the previous button again
    page.clickPreviousButton();
    // Then the page url should contain "page=1"
    cy.url().should( 'include', 'page=1' );
  } );
} );
