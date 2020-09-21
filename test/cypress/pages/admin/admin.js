export class AdminPage {
  open() {
    cy.visit( '/admin' );
  }

  login() {
    cy.get( '#id_username' ).type( 'admin' );
    cy.get( '#id_password' ).type( 'admin' );
    cy.get( 'form' ).submit();
  }

  pageList() {
    return cy.get( '.listing-page' );
  }

  openMostRecentPage() {
    this.pageList().find( 'a' ).first().click();
  }

  publishPage() {
    cy.get( '#page-edit-form' ).submit();
  }

  successBanner() {
    return cy.get( '.messages' ).find( '.success' );
  }

  openImageGallery() {
    cy.visit( '/admin/images/' );
  }

  getImages() {
    return cy.get( '#image-results' ).find( 'li' );
  }

  tags() {
    return cy.get( '.tagfilter' );
  }

  openDocumentsLibrary() {
    cy.visit( '/admin/documents/' );
  }

  getFirstDocument() {
    return cy.get( '#document-results' ).find( 'tr' ).eq( 1 );
  }

  openContacts() {
    this.openNavigationTab( 'Snippets' );
    this.selectSubMenu( 'Contacts' );
  }

  addContact() {
    cy.get( 'a[href="/admin/v1/contact/create/"]' ).click();
    cy.get( '#id_heading' ).type( 'Test heading' );
    cy.get( '.DraftEditor-root' ).type( 'Random Body' );
    this.submitForm();
  }

  openMortgageConstants() {
    this.openNavigationTab( 'Data Research' );
    this.selectSubMenu( 'Mortgage performance constants' );
  }

  addMortgageConstant() {
    cy.get( 'a[href="/admin/data_research/mortgagedataconstant/create/"]' ).click();
    cy.get( '#id_name' ).type( 'test' );
    this.submitForm();
  }

  openMortgageMetadata() {
    this.openNavigationTab( 'Data Research' );
    this.selectSubMenu( 'Mortgage metadata' );
  }

  addMortgageMetadata() {
    cy.get( 'a[href="/admin/data_research/mortgagemetadata/create/"]' ).click();
    cy.get( '#id_name' ).type( 'Test' );
    this.submitForm();
  }

  openNavigationTab( name ) {
    cy.get( '.nav-main' ).contains( name ).click();
  }

  selectSubMenu( name ) {
    cy.get( '.menu-item' ).contains( name ).click();
  }

  openRegulations() {
    this.openNavigationTab( 'Regulations' );
  }

  editRegulation() {
    this.getFirstTableRow().trigger( 'mouseover' );
    cy.get( 'a[href="/admin/regulations3k/part/edit/1/"]' ).click( { force: true } );
    this.submitForm();
  }

  copyRegulation() {
    this.getFirstTableRow().find( '.children' ).click();
    this.getFirstTableRow().contains( 'Copy' ).click( { force: true } );
    this.setRegulationEffectiveDate();
    this.submitForm();
  }

  cleanUpRegulations() {
    cy.get( 'table' ).find( 'tr' ).last().contains( 'Delete' ).click( { force: true } );
    this.submitForm();
  }

  setRegulationEffectiveDate() {
    cy.get( '#id_effective_date' ).clear().type( '2020-01-01' );
  }

  openMegaMenu() {
    this.openNavigationTab( 'Mega menu' );
  }

  editMegaMenu() {
    this.getFirstTableRow().contains( 'Edit' ).click( { force: true } );
    this.submitForm();
  }

  openPage( name ) {
    cy.get( '.c-explorer__item__link' ).contains( name ).click();
  }

  openCFGovPage() {
    this.openNavigationTab( 'Pages' );
    this.openPage( 'CFGov' );
  }

  addBlogChildPage() {
    cy.get( 'a' ).contains( 'Add child page' ).click();
    cy.get( 'a' ).contains( 'Blog page' ).click();
  }

  addFullWidthTextElement() {
    cy.get( '.action-add-block-full_width_text' ).click();
  }

  openBuildingBlockActivity() {
    this.openNavigationTab( 'TDP Activity' );
    this.selectSubMenu( 'Building Block' );
  }

  editBuildingBlock() {
    this.getFirstTableRow().contains( 'Edit' ).click( { force: true } );
    this.submitForm();
  }

  openApplicantTypes() {
    this.openNavigationTab( 'Job listings' );
    this.selectSubMenu( 'Applicant types' );
  }

  editApplicantType() {
    this.getFirstTableRow().contains( 'Edit' ).click( { force: true } );
    this.submitForm();
  }

  openFlag() {
    this.openNavigationTab( 'Settings' );
    this.selectSubMenu( 'Flags' );
    this.getFirstTableRow().find( 'a' ).first().click();
  }

  toggleFlag() {
    cy.get( 'table' ).siblings( 'a' ).first().click();
  }

  flagHeading() {
    return cy.get( '.help-block' );
  }

  openBlockInventory() {
    this.openNavigationTab( 'Settings' );
    this.selectSubMenu( 'Block Inventory' );
  }

  searchBlocks() {
    cy.get( '#id_form-0-block' ).select( 'ask_cfpb.models.blocks.AskContent' );
    cy.get( 'form[action="/admin/inventory/"]' ).submit(); // This form doesn't follow the standard Wagtail Format
  }

  searchResults() {
    return cy.get( '.listing' );
  }

  openExternalLinks() {
    this.openNavigationTab( 'External links' );
  }

  searchExternalLink( link ) {
    cy.get( '#id_url' ).type( link );
    this.submitForm();
  }

  openDjangoAdmin() {
    this.openNavigationTab( 'Django Admin' );
  }

  submitForm() {
    cy.get( 'form[method="POST"]' ).submit();
  }

  getFirstTableRow() {
    return cy.get( '.listing' ).find( 'tr' ).eq( 1 );
  }

  getPageMetadataReports() {
    this.openNavigationTab( 'Reports' );
    this.selectSubMenu( 'Page Metadata' );
    return cy.get( '.listing' ).find( 'tr' );
  }

  addTable() {
    cy.get( '.action-add-block-table_block' ).click();
  }

  selectFirstTableCell() {
    cy.get( '.htCore' ).find( 'td' ).first().click().click();
  }

  selectTableEditorButton( name ) {
    cy.get( '.modal-body' ).find( `[name="${ name }"]` ).click();
  }

  saveTableEditor() {
    // wait 1 second because editor has lag between input and appearing in editor
    cy.wait( 1000 );
    cy.get( '#table-block-save-btn' ).click();
  }

  selectTableEditorTextbox() {
    return cy.get( '.modal-body' ).find( '.public-DraftEditor-content' ).click();
  }

  typeTableEditorTextbox( text ) {
    return cy.get( '.modal-body' ).find( '.DraftEditor-editorContainer' ).type( text );
  }

  selectInternalLink( text ) {
    cy.get( '.choose-page' ).contains( text ).click();
  }

  selectDocumentLink( text ) {
    cy.get( '.document-choice' ).contains( text ).click();
  }
}
