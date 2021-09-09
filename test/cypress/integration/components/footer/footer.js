import { Footer } from './footer-helpers';

const page = new Footer();

describe( 'Footer', () => {
  it( 'Footer, at page load', () => {
    cy.visit( '/' );
    // Then the footer organism shouldn't display the Back to top button
    page.topButton().should( 'not.be.visible' );
    // And the footer organism should display the navigation list
    page.navList().should( 'be.visible' );
    // And the footer organism should display the middle "left" links
    page.middle( 'left' ).should( 'be.visible' );
    // And the footer organism should display the middle "right" links
    page.middle( 'right' ).should( 'be.visible' );
    // And the footer organism should display the social media icon list
    page.socialMediaIcons().should( 'be.visible' );
    // And the footer organism should display the official website text
    page.officialWebsite().should( 'be.visible' );
  } );
} );
