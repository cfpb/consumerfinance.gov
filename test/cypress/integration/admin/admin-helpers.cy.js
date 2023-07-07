export class AdminPage {
  login() {
    cy.session(
      'login',
      () => {
        this.open();
        this.submitLoginForm();
      },
      {
        validate() {
          cy.getCookie('sessionid').should('exist');
        },
      }
    );

    this.open();
  }

  open() {
    cy.visit('/admin/');
  }

  submitLoginForm() {
    cy.get('#id_username').type('admin');
    cy.get('#id_password').type('admin');
    cy.get('form').submit();
  }

  successBanner() {
    return cy.get('.messages').find('.success');
  }

  openImageGallery() {
    cy.visit('/admin/images/');
  }

  getImages() {
    return cy.get('#image-results').find('li');
  }

  tags() {
    return cy.get('.tagfilter');
  }

  openDocumentsLibrary() {
    cy.visit('/admin/documents/');
  }

  getFirstDocument() {
    return cy.get('#document-results').find('tr').eq(1);
  }

  openContacts() {
    this.openNavigationTab('Snippets');
    this.selectSubMenu('Contacts');
  }

  addContact() {
    cy.get('a[href="/admin/v1/contact/create/"]:first').click();
    cy.get('#id_heading').type('Test heading');
    cy.get('.DraftEditor-root').type('Random Body');
    this.submitForm();
  }

  searchContact(contact_heading) {
    cy.get('#changelist-search').type(contact_heading);
    cy.get('#changelist-search').type('{enter}');
  }

  removeContact() {
    cy.get('a[href^="/admin/v1/contact/delete/"]:first').click({ force: true });
    cy.get('[value="Yes, delete"]').click();
  }

  addMortgageData(name) {
    cy.get(
      `a[href="/admin/data_research/mortgage${name}/create/"]:first`
    ).click();
    cy.get('#id_name').type('test');
    this.submitForm();
  }

  openMortgageData(name) {
    this.openNavigationTab('Data Research');
    this.selectSubMenu(`Mortgage ${name}`);
  }

  openNavigationTab(name) {
    cy.get('.sidebar-menu-item').contains(name).click();
  }

  selectSubMenu(name) {
    cy.get('.sidebar-menu-item--in-sub-menu').contains(name).click();
  }

  openRegulations() {
    this.openNavigationTab('Regulations');
  }

  editRegulation() {
    this.getFirstTableRow().trigger('mouseover');
    cy.get('a[href^="/admin/regulations3k/part/edit/"]:first').click({
      force: true,
    });
    this.submitForm();
  }

  copyRegulation() {
    this.getFirstTableRow().find('.children').click();
    this.getFirstTableRow().contains('Copy').click({ force: true });
    this.setRegulationEffectiveDate('3099-01-01');
    this.submitForm();
  }

  cleanUpRegulations() {
    cy.get('table tr').last().contains('Delete').click({ force: true });
    this.submitForm();
  }

  setRegulationEffectiveDate(name) {
    cy.get('#id_effective_date').clear();
    cy.get('#id_effective_date').type(name);
  }

  openMegaMenu() {
    this.openNavigationTab('Mega menu');
  }

  editMegaMenu() {
    this.getFirstTableRow().contains('Edit').click({ force: true });
    this.submitForm();
  }

  openPage(name) {
    this.openNavigationTab('Pages');
    cy.get('.c-explorer__item__link').contains(name).click({ force: true });
  }

  addBlogChildPage() {
    cy.visit('/admin/pages/add/v1/blogpage/1/');
    cy.url().should('include', 'blogpage');
  }

  clickBlock(name) {
    const block = `.action-add-block-${name}`;
    cy.get(block).scrollIntoView();
    cy.get(block).should('be.visible');
    return cy.get(block).click();
  }

  addFullWidthText() {
    this.clickBlock('full_width_text');
  }

  openBuildingBlockActivity() {
    this.openNavigationTab('TDP Activity');
    this.selectSubMenu('Building Block');
  }

  editBuildingBlock() {
    this.getFirstTableRow().contains('Edit').click({ force: true });
    this.submitForm();
  }

  openApplicantTypes() {
    this.openNavigationTab('Job listings');
    this.selectSubMenu('Applicant types');
  }

  editApplicantType() {
    this.getFirstTableRow().contains('Edit').click({ force: true });
    this.submitForm();
  }

  openFlag() {
    this.openNavigationTab('Settings');
    this.selectSubMenu('Flags');
    this.getFirstTableRow().find('a').first().click();
  }

  toggleFlag() {
    cy.get('.flag > a').first().click();
  }

  flagHeading() {
    return cy.get('.help-block');
  }

  openBlockInventory() {
    this.openNavigationTab('Reports');
    this.selectSubMenu('Block Inventory');
  }

  searchResults() {
    return cy.get('.listing');
  }

  searchExternalLink(link) {
    cy.get('#id_url').type(link);
    this.submitForm();
  }

  openDjangoAdmin() {
    this.openNavigationTab('Django Admin');
  }

  submitForm() {
    cy.get('form[method="POST"]').submit();
  }

  getFirstTableRow() {
    return cy.get('.listing tr').eq(1);
  }

  getPageMetadataReports() {
    this.openNavigationTab('Reports');
    this.selectSubMenu('Page Metadata');
    return cy.get('.listing').find('tr');
  }

  addTable() {
    cy.get('input[value="table_block"]', { timeout: 1000 }).should('not.exist');
    this.clickBlock('table_block');
    cy.get('input[value="table_block"]', { timeout: 1000 }).should('exist');
  }

  getFirstTableCell() {
    return cy.get('.htCore td').first();
  }

  getTableEditor() {
    cy.get('.handsontableInputHolder', { timeout: 60000 })
      // Make sure the editor isn't hidden
      .should('not.have.css', 'z-index', '-1')
      .as('tableEditor');
  }

  editFirstTableCell() {
    cy.get('.htCore td').first().as('firstTableCell');

    cy.get('@firstTableCell').scrollIntoView({ duration: 1000 });

    /* We need to click near the top left of the cell. */
    cy.get('@firstTableCell').dblclick(5, 5, { force: true });
    this.getTableEditor();
  }

  selectTableEditorButton(name) {
    // Type a slash to open the popup menu.
    cy.get('@tableEditor').find('.public-DraftEditor-content').focus();
    cy.get('@tableEditor').find('.public-DraftEditor-content').type('/');

    // Then click on the item we want.
    cy.get('.Draftail-ComboBox__option-text').contains(name).click();
  }

  searchFirstTableCell(name) {
    return cy.get('@firstTableCell').contains(name);
  }

  closeTableEditor() {
    /* Clicking anywhere outside the editor closes it, so we'll just click
       on the very bottom right of the content container */
    cy.get('.content').click('bottomRight', { force: true });
  }

  typeTableEditorTextbox(text) {
    cy.get('@tableEditor').find('.public-DraftEditor-content').focus();
    return cy
      .get('@tableEditor')
      .find('.public-DraftEditor-content')
      .type(text);
  }
}
