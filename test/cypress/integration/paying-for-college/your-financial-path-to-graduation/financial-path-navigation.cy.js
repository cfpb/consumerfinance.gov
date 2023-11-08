import { PfcFinancialPathToGraduation } from './financial-path-helpers.cy.js';

const page = new PfcFinancialPathToGraduation();

describe('Your Financial Path to Graduation (navigation)', () => {
  beforeEach(() => {
    cy.visit('/paying-for-college/your-financial-path-to-graduation/');
    page.clickGetStarted();
  });

  it('should not navigate when program radios are not selected', () => {
    page.enter('Harvard University');
    page.searchResults().should('be.visible');
    page.clickSearchResult('Harvard University');

    page.clickNextStep();
    cy.get('#college-costs_school-search').should('be.visible');
    page.clickLeftNav('costs');
    cy.get('#college-costs_school-search').should('be.visible');
  });

  it('should navigate the sections properly using the left-side nav', () => {
    page.enterProgramDetails();

    page.clickLeftNav('costs');
    cy.get('[data-tool-section="costs"]').should('be.visible');
    page.clickLeftNav('grants-scholarships');
    cy.get('[data-tool-section="grants-scholarships"]').should('be.visible');
    page.clickLeftNav('work-study');
    cy.get('[data-tool-section="work-study"]').should('be.visible');
  });

  it('should show and hide the submenus of the secondary nav properly', () => {
    page.enterProgramDetails();
    page.clickLeftNav('costs');
    cy.get('[data-nav_item="loan-counseling"]').should('not.be.visible');
    cy.get('[data-nav_section="covering-costs"]').click();
    cy.get('[data-nav_item="loan-counseling"]').should('be.visible');
  });

  it('should properly handle cost inputs', () => {
    page.enterProgramDetails();

    page.clickLeftNav('costs');
    cy.get('#costs-offer-button').click();
    cy.get('#costs_inputs-section').should('not.be.visible');

    page.costsQuestionChoice('yes');
    cy.get('#costs_inputs-section').should('be.visible');

    page.clickNextStep();
    cy.get('[data-tool-section="grants-scholarships"]').should('be.visible');
  });
});
