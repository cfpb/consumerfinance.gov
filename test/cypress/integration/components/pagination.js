import { Pagination } from '../../components/pagination';

const page = new Pagination();

describe( 'Pagination molecule to navigate on the filterable pages', () => {
  before( () => {
    cy.visit( '/about-us/blog/' );
  } );
  it( 'should be able to navigate to the next page', () => {
    // When I click on the "next" button
    page.clickButton( 'next' );
    // Then the page url should contain "page=2"
    cy.url().should( 'include', 'page=2' );
  } );
  it( 'should be able to navigate to the previous page', () => {
    page.clickButton( 'prev' );
    // Then the page url should contain "page=1"
    cy.url().should( 'include', 'page=1' );
  } );
  it( 'should be able to navigate to a specific page', () => {
    // When I enter "3" in the page input field
    page.enter( '3' );
    // And I click on the "submit" button
    page.clickButton( 'submit' );
    // Then the page url should contain "page=3"
    cy.url().should( 'include', 'page=3' );
  } );
} );
