import { Header } from './header-helpers';
import { MegaMenu } from './mega-menu-helpers';

const page = new Header();
const menu = new MegaMenu();

describe( 'Header', () => {
  before( () => {
    cy.visit( '/' );
  } );
  it( 'Header, at page load', () => {
    // Then the header organism should display the content
    page.headerContent().should( 'be.visible' );
    // And the header organism should display the logo
    page.headerLogo().should( 'be.visible' );
    // And the header organism shouldn't display the overlay
    page.overlay().should( 'not.be.visible' );
    // And the header organism shouldn't display the mega menu
    page.megaMenuHeader().should( 'not.exist' );
    // And the header organism should display the global search
    page.globalSearch().should( 'be.visible' );
    // And the header organism should display the global eyebrow horizontal
    menu.globalEyebrowHorizontal().should( 'be.visible' );
    // And the header organism should display the global header Cta
    page.globalHeaderCta().should( 'be.visible' );
    // And the header organism should display the mega menu content link
    menu.megaMenuContent( 'link' ).should( 'be.visible' );
    // And the header organism shouldn't display the global eyebrow list
    menu.globalEyebrowList().should( 'not.be.visible' );
  } );
  it( 'Header, if you click the mega-menu trigger', () => {
    // When I click on the first mega-menu trigger
    menu.trigger().first().click( { force: true } );
    // Then the header organism should display the mega menu content
    menu.contentLink( '1' ).should( 'be.visible' );
    // When I click on the last mega-menu trigger
    menu.trigger().last().click( { force: true } );
    // Then the header organism should display the mega menu content
    menu.contentLink( '2' ).should( 'be.visible' );
    // Then the header organism should display the global eyebrow horizontal
    menu.globalEyebrowHorizontal().should( 'be.visible' );
    // Then the header organism should display the global eyebrow list
    menu.globalEyebrowList().should( 'not.be.visible' );
  } );
  it( 'Header, if you click mega-menu, and you click search', () => {
    // When I click on the mega-menu trigger
    menu.trigger().first().click( { force: true } );
    // Then the header organism should display content
    menu.content().should( 'be.visible' );
    // When I click on the mega-menu search trigger
    page.globalSearchTrigger().click( { force: true } );
    // Then the mega-menu search form should be displayed
    page.globalSearchContent().should( 'be.visible' );
    // And the mega-menu shouldn't display content overview
    menu.contentOverviewLink( '1' ).should( 'not.exist' );
  } );
} );
