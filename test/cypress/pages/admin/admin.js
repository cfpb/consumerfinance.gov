export class AdminPage {
  open() {
    cy.visit( '/login/' );
  }

  login() {
    cy.get( '#id_username' ).type( 'admin' );
    cy.get( '#id_password' ).type( 'admin' );
    cy.get( 'form' ).submit();
  }

  openMostRecentPage() {
    cy.get( '.listing-page a' ).first().click();
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

  addMortgageData( name ) {
    cy.get( `a[href="/admin/data_research/mortgage${ name }/create/"]` )
      .click();
    cy.get( '#id_name' ).type( 'test' );
    this.submitForm();
  }

  openMortgageData( name ) {
    this.openNavigationTab( 'Data Research' );
    this.selectSubMenu( `Mortgage ${ name }` );
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
    cy.get( 'a[href="/admin/regulations3k/part/edit/1/"]' )
      .click( { force: true } );
    this.submitForm();
  }

  copyRegulation() {
    this.getFirstTableRow().find( '.children' ).click();
    this.getFirstTableRow().contains( 'Copy' ).click( { force: true } );
    this.setRegulationEffectiveDate( '2020-01-01' );
    this.submitForm();
  }

  cleanUpRegulations() {
    cy.get( 'table tr' ).last().contains( 'Delete' ).click( { force: true } );
    this.submitForm();
  }

  setRegulationEffectiveDate( name ) {
    cy.get( '#id_effective_date' ).clear().type( name );
  }

  openMegaMenu() {
    this.openNavigationTab( 'Mega menu' );
  }

  editMegaMenu() {
    this.getFirstTableRow().contains( 'Edit' ).click( { force: true } );
    this.submitForm();
  }

  openPage( name ) {
    this.openNavigationTab( 'Pages' );
    cy.get( '.c-explorer__item__link' ).contains( name )
      .click( { force: true } );
  }

  addBlogChildPage() {
    cy.visit( '/admin/pages/add/v1/blogpage/319/' );
    cy.url().should( 'include', 'blogpage' );
  }

  clickBlock( name ) {
    return cy.get( `.action-add-block-${ name }`, { timeout: 60000 } )
      .should( 'be.visible' )
      .click();
  }

  addFullWidthText() {
    this.clickBlock( 'full_width_text' );
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
    // This form doesn't follow the standard Wagtail Format
    cy.get( 'form[action="/admin/inventory/"]' ).submit();
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
    return cy.get( '.listing tr' ).eq( 1 );
  }

  getPageMetadataReports() {
    this.openNavigationTab( 'Reports' );
    this.selectSubMenu( 'Page Metadata' );
    return cy.get( '.listing' ).find( 'tr' );
  }

  addTable() {
    this.clickBlock( 'table_block' );
    cy.get( '.c-sf-container__block-container', { timeout: 60000 } )
      .should( 'be.visible' );
    cy.get( '.c-sf-add-panel__grid', { timeout: 60000 } )
      .should( 'be.visible' );
  }

  getFirstTableCell() {
    return cy.get( '.htCore td' ).first();
  }

  getTableModal() {
    // Retry while element css has the "display: none" property
    cy.get( '.table-block-modal', { timeout: 60000 } )
      .should( 'not.have.css', 'display', 'none' )
      .as( 'tableModal' );
  }

  selectFirstTableCell() {
    cy.get( '.htCore td' ).first().as( 'firstTableCell' );
    cy.get( '@firstTableCell' ).click( { force: true } ).click( { force: true } );
    this.getTableModal();
  }

  selectTableEditorButton( name ) {
    cy.get( '@tableModal' ).find( `[name="${ name }"]` )
      .click( { force: true } );
  }

  searchFirstTableCell( name ) {
    return cy.get( '@firstTableCell' ).contains( name );
  }

  closeTableEditor() {
    cy.get( '#close-table-block-modal-btn' ).click( { force: true } );
  }

  saveTableEditor() {
    // Wait for editor to register entered text before saving.
    cy.wait( 1000 );
    cy.get( '@tableModal', { timeout: 60000 } )
      .should( 'be.visible' )
      .find( '#table-block-save-btn' )
      .click();
  }

  selectTableEditorTextbox() {
    return cy.get( '@tableModal' )
      .find( '.public-DraftEditor-content' )
      .click();
  }

  typeTableEditorTextbox( text ) {
    /* Wait for Wagtail JS to finish initializing.
       If we don't, it interrupts the typing. */
    return cy.get( '.public-DraftEditor-content' )
      .last().focus().type( text, { force: true } );
  }

  selectInternalLink( text ) {
    cy.get( '.choose-page' ).contains( text ).click();
  }

  selectDocumentLink( text ) {
    cy.get( '#id_q' ).invoke( 'val', text ).trigger( 'change' );
    cy.get( '#id_q' ).type( ' ' );
    cy.get( '#id_q' ).type( '{enter}' );
    cy.wait( 1000 );
    cy.get( '.document-choice' ).should( 'contain', text );
    cy.get( '#search-results' ).should( 'contain', 'There is 1 match' );
    cy.get( '#search-results', { timeout: 10000 } ).contains( text ).click();
  }
}
