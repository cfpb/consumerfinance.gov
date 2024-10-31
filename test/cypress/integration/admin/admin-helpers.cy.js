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
      },
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
    return cy.get('#listing-results').find('li');
  }

  filters() {
    return cy.get('.w-filter-button');
  }

  openDocumentsLibrary() {
    cy.visit('/admin/documents/');
  }

  getFirstDocument() {
    return cy.get('#listing-results').find('tr').eq(1);
  }

  openContacts() {
    this.openNavigationTab('Snippets');
    this.selectSubMenu('Contacts');
  }

  addContact(heading) {
    cy.get('a[href="/admin/snippets/v1/contact/add/"]:first').click();
    cy.get('#id_heading').type(heading);
    cy.get('.DraftEditor-root').type('Random Body');
    this.submitForm();
  }

  searchContact(heading) {
    cy.get('#id_q').type(heading);
    cy.get('#id_q').type('{enter}');
  }

  getFirstOptionsDropdown() {
    return cy.get(`button[aria-label^="More options for"]`).eq(0);
  }

  removeContact() {
    this.getFirstOptionsDropdown().click();
    cy.get('a[href^="/admin/snippets/v1/contact/delete/"]:first').click();
    cy.get('[value="Yes, delete"]').click();
  }

  addMortgageData(name) {
    cy.get(
      `a[href="/admin/snippets/data_research/mortgage${name}/add/"]:first`,
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
    this.getFirstTableRow().find('.children a').click();
    this.getFirstTableRow().contains('Copy').should('be.visible');
    this.getFirstTableRow().contains('Copy').click();
    this.setRegulationEffectiveDate('3099-01-01');
    this.submitForm();
  }

  cleanUpRegulations() {
    cy.get('table.listing tr').last().contains('Delete').click({ force: true });
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
    this.getFirstOptionsDropdown('English').click();
    this.getFirstTableRow().contains('Edit').click({ force: true });
    this.submitForm();
  }

  openBuildingBlockActivity() {
    this.openNavigationTab('TDP Activity');
    this.selectSubMenu('Building Block');
  }

  editBuildingBlock() {
    this.getFirstOptionsDropdown().click();
    this.getFirstTableRow().contains('Edit').click({ force: true });
    this.submitForm();
  }

  openApplicantTypes() {
    this.openNavigationTab('Job listings');
    this.selectSubMenu('Applicant types');
  }

  editApplicantType() {
    this.getFirstOptionsDropdown().click();
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
    cy.get('main form[method="POST"]:not(.w-editing-sessions)').submit();
  }

  getFirstTableRow() {
    return cy.get('.listing tr').eq(1);
  }

  getPageMetadataReports() {
    this.openNavigationTab('Reports');
    this.selectSubMenu('Page Metadata');
    return cy.get('.listing').find('tr');
  }

  addSublandingPage() {
    cy.visit('/admin/pages/add/v1/sublandingpage/1/');
    cy.url().should('include', 'sublandingpage');
  }

  clickBlock(name) {
    cy.get('div[data-contentpath="content"] .c-sf-add-button').should(
      'be.visible',
    );
    cy.get('div[data-contentpath="content"] .c-sf-add-button').click();

    cy.contains('div.w-combobox__option', name).should('be.visible');
    return cy.contains('div.w-combobox__option', name).click();
  }

  addTable() {
    cy.get('input[value="table"]', { timeout: 1000 }).should('not.exist');
    this.clickBlock('Table');
    cy.get('input[value="table"]', { timeout: 1000 }).should('exist');
  }

  setClipboard(text) {
    cy.window().its('navigator.clipboard').invoke('writeText', text);
  }

  getTableHeadingCell() {
    return cy.get('input[name="content-0-value-data-column-0-heading"]');
  }

  getTableDataCell() {
    return cy.get('input[name="content-0-value-data-cell-0-1"]');
  }

  getTableData() {
    return '00\t01\n10\t11\n';
  }

  pasteTableAsText() {
    cy.get('button.paste-as-text').click();
  }

  pasteTableAsRichText() {
    cy.get('button.paste-as-rich-text').click();
  }
}
