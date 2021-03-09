import { MegaMenu } from '../../components/mega-menu';

const menu = new MegaMenu();

describe( 'Mega-Menu organism for site navigation', () => {
  before( () => {
    cy.visit( '/' );
  } );
  it( 'Mega-Menu, on page Load', () => {
    // Then the mega-menu organism should not show content
    menu.contentLink( '2' ).should( 'not.be.visible' );
  } );
  it( 'Mega-Menu, mouse moves between menu items', () => {
    // When mouse moves from one link to another
    menu.clickLink( '1' );
    // Then should only show first link content
    menu.contentLink( '1' ).should( 'exist' );
    // When mouse moves from one link to another
    menu.clickLink( '2' );
    // Then should only show second link content
    menu.contentLink( '2' ).should( 'exist' );
  } );
  it( 'Mega-Menu, mouse click on menu items', () => {
    // Then the mega-menu organism should show menu when clicked
    menu.triggerOpen();
    // Then the mega-menu organism should show not show menu when clicked
    menu.triggerClose();
    // Then the mega-menu organism should show menu content when clicked
    menu.contentValueListGroup( '1' ).should( 'be.visible' );
    // Then the mega-menu organism should show not menu content when clicked
    menu.contentValueListGroup( '2' ).should( 'not.be.visible' );
    // Then the mega-menu organism should shift menus when tabbing multiple times
    menu.tabbing();
    menu.globalEyebrowElement().should( 'be.visible' );
    // Then the global-eyebrow organism should show languages when clicked
    menu.globalEyebrowLanguages().should( 'exist' );
    menu.globalEyebrow( 'actions' ).should( 'exist' );
    menu.globalEyebrow( 'phone' ).should( 'be.visible' );
  } );
} );
