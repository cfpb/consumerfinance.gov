import { AdminPage } from './admin-helpers';

const admin = new AdminPage();

describe( 'Admin', () => {

  before( () => {
    cy.viewport( 'macbook-13' );
    admin.open();
    admin.login();
  } );

  beforeEach( () => {
    /* Preserve the 'sessionid' cookie so it will not be cleared
       before the NEXT test starts. */
    Cypress.Cookies.preserveOnce( 'sessionid' );
    cy.viewport( 'macbook-13' );
  } );

  it( 'should login', () => {
    cy.contains( 'Welcome' );
  } );

  it( 'should be able to publish a page', () => {
    admin.openMostRecentPage();
    admin.publishPage();
    admin.successBanner().should( 'be.visible' );
  } );

  it( 'should be able to open the Images library', () => {
    admin.openImageGallery();
    admin.getImages().should( 'be.visible' );
    admin.tags().should( 'contain', 'Mortgages' );
  } );

  it( 'should be able to open the Documents library', () => {
    admin.openDocumentsLibrary();
    admin.getFirstDocument().should( 'be.visible' );
  } );

  it( 'should add a Contact Snippet', () => {
    admin.openContacts();
    admin.addContact();
    admin.successBanner().should( 'be.visible' );
  } );

  it( 'should add mortage constant', () => {
    admin.openMortgageData( 'performance constants' );
    admin.addMortgageData( 'dataconstant' );
    admin.successBanner().should( 'be.visible' );
  } );

  it( 'should add mortgage metadata', () => {
    admin.openMortgageData( 'metadata' );
    admin.addMortgageData( 'metadata' );
    admin.successBanner().should( 'be.visible' );
  } );

  it( 'should edit an existing regulation', () => {
    admin.openRegulations();
    admin.editRegulation();
    admin.successBanner().should( 'be.visible' );
  } );

  it( 'should copy an existing regulation', () => {
    admin.openRegulations();
    admin.copyRegulation();
    admin.successBanner().should( 'be.visible' );
    admin.cleanUpRegulations();
    admin.successBanner().should( 'be.visible' );
  } );

  it( 'should edit the Mega Menu', () => {
    admin.openMegaMenu();
    admin.editMegaMenu();
    admin.successBanner().should( 'be.visible' );
  } );

  it( 'should be able to modify TDP activities', () => {
    admin.openBuildingBlockActivity();
    admin.editBuildingBlock();
    admin.successBanner().should( 'be.visible' );
  } );

  it( 'should be able to modify Applicant Types', () => {
    admin.openApplicantTypes();
    admin.editApplicantType();
    admin.successBanner().should( 'be.visible' );
  } );

  it( 'should be able to toggle a flag', () => {
    admin.openFlag();
    admin.toggleFlag();
    admin.flagHeading().should( 'contain', 'enabled for all requests' );
    admin.toggleFlag();
    admin.flagHeading().should( 'contain', 'enabled when any condition is met.' );
  } );

  it( 'should use Block Inventory to search for blocks', () => {
    admin.openBlockInventory();
    admin.searchBlocks();
    admin.searchResults().should( 'be.visible' );
  } );

  it( 'Should be able to search for external links', () => {
    admin.openExternalLinks();
    admin.searchExternalLink( 'https://www.federalreserve.gov' );
    admin.searchResults().should( 'be.visible' );
  } );

  it( 'should run Page Metadata report', () => {
    admin.getPageMetadataReports().its( 'length' ).should( 'be.gt', 2 );
  } );

  it( 'should open the Django Admin', () => {
    admin.openDjangoAdmin();
    cy.url().should( 'contain', 'django-admin' );
    cy.visit( '/admin/' );
  } );

  describe( 'Custom TableBlock', () => {
    before( () => {
      admin.addBlogChildPage();
      admin.addFullWidthText();
      admin.addTable();
    } );

    beforeEach( () => {
      admin.editFirstTableCell();
    } );

    it( 'should be able to create and edit a table', () => {
      const text = 'test cell text';
      admin.typeTableEditorTextbox( text );
      admin.closeTableEditor();
      admin.searchFirstTableCell( text ).should( 'be.visible' );
    } );

    it( 'should be able to select all standard edit buttons in table', () => {
      admin.selectTableEditorButton( 'BOLD' );
      admin.selectTableEditorButton( 'ITALIC' );
      admin.selectTableEditorButton( 'header-three' );
      admin.selectTableEditorButton( 'header-four' );
      admin.selectTableEditorButton( 'header-five' );
      admin.selectTableEditorButton( 'ordered-list-item' );
      admin.selectTableEditorButton( 'unordered-list-item' );
      admin.selectTableEditorButton( 'undo' );
      admin.selectTableEditorButton( 'redo' );
      admin.closeTableEditor();
    } );

    it( 'should be able to use link buttons', () => {
      admin.selectTableEditorButton( 'LINK' );
      admin.selectInternalLink( 'CFGov' );
      const documentName = 'cfpb_interested-vendor-instructions_fy2020.pdf';
      admin.selectTableEditorButton( 'DOCUMENT' );
      admin.selectDocumentLink( documentName );
      admin.closeTableEditor();
    } );

    it( 'should be able to save an empty cell', () => {
      admin.typeTableEditorTextbox( '{selectall} ' );
      admin.closeTableEditor();
      admin.getFirstTableCell().should( 'be.empty' );
    } );
  } );
} );
