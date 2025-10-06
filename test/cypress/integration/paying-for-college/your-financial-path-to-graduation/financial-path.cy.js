import { PfcFinancialPathToGraduation } from './financial-path-helpers.cy.js';

const page = new PfcFinancialPathToGraduation();

const apiConstants =
  '/paying-for-college2/understanding-your-financial-aid-offer/api/constants/';
const apiSchoolOne =
  '/paying-for-college2/understanding-your-financial-aid-offer/api/school/166027/';

/**
 *
 */
describe('Paying For College', () => {
  beforeEach(() => {
    cy.intercept('GET', apiConstants, {
      host: 'localhost',
      fixture: 'paying-for-college/constants.json',
    });
    cy.intercept('GET', apiSchoolOne, {
      host: 'localhost',
      fixture: 'paying-for-college/school-166027.json',
    });

    cy.visit('/paying-for-college/your-financial-path-to-graduation/');
  });

  describe('Your Financial Path To Graduation', () => {
    it('college search should show results only for 3+ chars', () => {
      page.clickGetStarted();
      page.enter('un');
      page.searchResults().should('not.be.visible');
      page.enter('uni');
      page.searchResults().should('be.visible');
      page.typeText('search__school-input', '{backspace}');
      page.searchResults().should('not.be.visible');
    });
    it('American college search should return results', () => {
      page.clickGetStarted();
      page.enter('American');
      page.searchResults().should('be.visible');
    });
    it('Selecting college should add its details to the DOM', () => {
      page.clickGetStarted();
      page.enter('Harvard University');
      page.searchResults().should('be.visible');
      page.clickSearchResult('Harvard University');
      cy.get('[data-school-item="school"]').should(
        'contain',
        'Harvard University',
      );
      cy.get('[data-school-item="city"]').should('contain', 'Cambridge');
      cy.get('[data-school-item="state"]').should('contain', 'MA');
      cy.get('[data-school-item="control"]').should('contain', 'Private');
    });
    it('should advance with income set', () => {
      page.clickGetStarted();
      page.enter('Harvard University');
      page.searchResults().should('be.visible');
      page.clickSearchResult('Harvard University');
      page.setIncome('48k-75k');
      page.nextToSchoolCosts();
      cy.get('.college-costs__tool-section--school-costs.active').should(
        'be.visible',
      );
      cy.get('span[data-financial-item="total_costOfProgram"]').should(
        'contain',
        '$2,152',
      );
    });
    it('does not advance without valid selections', () => {
      page.clickGetStarted();
      page.nextToSchoolCosts();
      cy.get('.college-costs__tool-section--school-costs.active').should(
        'not.exist',
      );
      cy.get('div[data-state-based-visibility="school-fields-errors"]').should(
        'be.visible',
      );

      page.clickLeftNav('estimate-debt');

      cy.get('div[data-state-based-visibility="school-fields-errors"]').should(
        'be.visible',
      );

      page.chooseAndSet();

      page.clickLeftNav('estimate-debt');

      cy.get('div[data-state-based-visibility="school-fields-errors"]').should(
        'not.be.visible',
      );

      page.skipToCustomized();
      cy.get('.college-costs__tool-section--make-a-plan.active').should(
        'exist',
      );
    });

    it('uses net price to calculate payments if not customizing', () => {
      page.clickGetStarted();

      page.chooseAndSet();

      page.clickLeftNav('affording-payments');

      cy.get('[data-financial-item="debt_tenYearMonthly"]').should(
        'contain',
        '$26',
      );
    });

    it('uses total cost to calculate payments if customizing', () => {
      page.clickGetStarted();

      page.chooseAndSet();

      page.clickLeftNav('customize-estimate');

      page.nextToSeeCustomized();

      page.clickLeftNav('affording-payments');

      cy.get('[data-financial-item="debt_tenYearMonthly"]').should(
        'contain',
        '$3,518',
      );
    });
  });
});
