import { AdminPage } from './admin-helpers.cy.js';

const admin = new AdminPage();

describe('Admin', () => {
  beforeEach(() => {
    /* We can be reasonably sure that the Wagtail admin is being used on a
      laptop screen or larger, and the table editor is wider than Cypress's
      default viewport, so we'll size the viewport appropriately */
    cy.viewport('macbook-13');

    admin.login();
  });

  it('should login', () => {
    cy.contains('Welcome');
  });

  it('should be able to open the Images library', () => {
    admin.openImageGallery();
    admin.getImages().should('be.visible');
    admin.filters().should('be.visible');
  });

  it('should be able to open the Documents library', () => {
    admin.openDocumentsLibrary();
    admin.getFirstDocument().should('be.visible');
  });

  it('should add a Contact Snippet', () => {
    const heading = 'Test heading';
    admin.openContacts();
    admin.addContact(heading);
    admin.successBanner().should('be.visible');
    admin.searchContact(heading);
    admin.removeContact();
    admin.successBanner().should('be.visible');
  });

  it('should add mortage constant', () => {
    admin.openMortgageData('performance constants');
    admin.addMortgageData('dataconstant');
    admin.successBanner().should('be.visible');
  });

  it('should add mortgage metadata', () => {
    admin.openMortgageData('metadata');
    admin.addMortgageData('metadata');
    admin.successBanner().should('be.visible');
  });

  it('should edit an existing regulation', () => {
    admin.openRegulations();
    admin.editRegulation();
    admin.successBanner().should('be.visible');
  });

  it('should copy an existing regulation', () => {
    admin.openRegulations();
    admin.copyRegulation();
    admin.successBanner().should('be.visible');
    admin.cleanUpRegulations();
    admin.successBanner().should('be.visible');
  });

  it('should edit the Mega Menu', () => {
    admin.openMegaMenu();
    admin.editMegaMenu();
    admin.successBanner().should('be.visible');
  });

  it('should be able to modify TDP activities', () => {
    admin.openBuildingBlockActivity();
    admin.editBuildingBlock();
    admin.successBanner().should('be.visible');
  });

  it('should be able to modify Applicant Types', () => {
    admin.openApplicantTypes();
    admin.editApplicantType();
    admin.successBanner().should('be.visible');
  });

  it('should be able to toggle a flag', () => {
    admin.openFlag();
    admin.flagHeading().then((heading) => {
      admin.toggleFlag();
      admin.flagHeading().should('not.contain', heading.get(0).innerText);
      // reset flag to what it was before. Only works locally.
      admin.toggleFlag();
    });
  });

  it('should access the Block Inventory and verify results', () => {
    admin.openBlockInventory();
    admin.searchResults().should('be.visible');
  });

  it('should run Page Metadata report', () => {
    admin.getPageMetadataReports().its('length').should('be.gt', 2);
  });

  it('should open the Django Admin', () => {
    admin.openDjangoAdmin();
    cy.url().should('contain', 'django-admin');
    cy.visit('/admin/');
  });
});

// Access to the clipboard works consistently in Electron but asks the user for
// permission in other browsers, like Chrome. Only run these tests in Electron.
describe('Pasting into tables', { browser: 'electron' }, () => {
  beforeEach(() => {
    admin.login();
    admin.addSublandingPage();
    admin.addTable();

    admin.getTableHeadingCell().should('not.exist');
    admin.getTableDataCell().should('not.exist');
  });

  it('should gracefully handle non-table data on the clipboard', () => {
    admin.setClipboard('This is not a table.\n');
    admin.pasteTableAsText();

    admin.getTableHeadingCell().should('not.exist');
    admin.getTableDataCell().should('not.exist');
  });

  it('should create a text table by pasting from the clipboard', () => {
    admin.setClipboard(admin.getTableData());
    admin.pasteTableAsText();

    admin.getTableHeadingCell().should('exist').should('have.value', '00');
    admin.getTableDataCell().should('exist').should('have.value', '11');
  });

  it('should create a rich text table by pasting from the clipboard', () => {
    admin.setClipboard(admin.getTableData());
    admin.pasteTableAsRichText();

    admin.getTableHeadingCell().should('exist').should('have.value', '00');
    admin.getTableDataCell().should(($input) => {
      expect($input.val()).to.contain('"text":"11"');
    });
  });
});
