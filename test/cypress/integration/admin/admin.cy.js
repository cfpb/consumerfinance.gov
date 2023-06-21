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
    admin.tags().should('be.visible');
  });

  it('should be able to open the Documents library', () => {
    admin.openDocumentsLibrary();
    admin.getFirstDocument().should('be.visible');
  });

  it('should add a Contact Snippet', () => {
    admin.openContacts();
    admin.addContact();
    admin.successBanner().should('be.visible');
    admin.searchContact('Test heading');
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

  describe('Custom TableBlock', () => {
    beforeEach(() => {
      admin.login();
      admin.addBlogChildPage();
      admin.addFullWidthText();
      admin.addTable();
      admin.editFirstTableCell();
    });

    it('should be able to create and edit a table', () => {
      const text = 'test cell text';
      admin.typeTableEditorTextbox(text);
      admin.closeTableEditor();
      admin.searchFirstTableCell(text).should('be.visible');
    });

    it('should be able to insert a block into a table', () => {
      admin.selectTableEditorButton('Heading 3');
      admin.selectTableEditorButton('Heading 4');
      admin.selectTableEditorButton('Heading 5');
      admin.selectTableEditorButton('Numbered list');
      admin.selectTableEditorButton('Bulleted list');
      admin.closeTableEditor();
    });

    it('should be able to save an empty cell', () => {
      admin.typeTableEditorTextbox('{selectall} ');
      admin.closeTableEditor();
      admin.getFirstTableCell().should('be.empty');
    });
  });
});
