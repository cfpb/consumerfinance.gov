import { AdminPage } from '../../pages/admin/admin';

const admin = new AdminPage();

describe( 'Admin', () => {

  beforeEach( () => {
    admin.open();
    admin.login();
  } );

  it( 'should login', () => {
    cy.contains( 'Welcome' );
  } );

  it( 'should be able to edit a page', () => {
    admin.openMostRecentPage();
    admin.publishPage();
    admin.successBanner().should( 'be.visible' );
  } );

  it( 'should be able to open the image gallery', () => {
    admin.openImageGallery();
    admin.getImages().should( 'be.visible' );
    admin.tags().should( 'contain', 'Mortgages' );
  } );

  it( 'should be able to open the document library', () => {
    admin.openDocumentsLibrary();
    admin.getFirstDocument().should( 'be.visible' );
  } );

  it( 'should support our snippet libraries', () => {
    admin.openContacts();
    admin.addContact();
    admin.successBanner().should( 'be.visible' );
  } );

  it( 'should have mortage constants stored', () => {
    admin.openMortgageConstants();
    admin.addMortgageConstant();
    admin.successBanner().should( 'be.visible' );
  } );

  it( 'should have mortgage metadata', () => {
    admin.openMortgageMetadata();
    admin.addMortgageMetadata();
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

  it( 'should be able to modify tdp activities', () => {
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

  it( 'should support the block inventory', () => {
    admin.openBlockInventory();
    admin.searchBlocks();
    admin.searchResults().should( 'be.visible' );
  } );

  it( 'Should support external links', () => {
    admin.openExternalLinks();
    admin.searchExternalLink( 'https://www.federalreserve.gov' );
    admin.searchResults().should( 'be.visible' );
  } );

  it( 'should open the django admin', () => {
    admin.openDjangoAdmin();
    cy.url().should( 'contain', 'django-admin' );
  } );

  it( 'should include the page metadata report', () => {
    admin.getPageMetadataReports().its( 'length' ).should( 'be.gt', 2 );
  } );

} );
