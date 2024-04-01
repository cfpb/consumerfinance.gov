import { ExploreCreditCards } from './explore-cards-helpers.cy.js';

const exploreCards = new ExploreCreditCards();

describe('Explore credit cards landing page', () => {
  it('should show results tailored to the selected situation', () => {
    exploreCards.openLandingPage();

    exploreCards.selectLocation('NY');
    exploreCards.selectSituation('Earn rewards');
    exploreCards.clickSubmitButton();

    exploreCards.openFilterExpandable();

    cy.get('#id_rewards input').should('be.checked');
  });
});

describe('Explore credit cards results page', () => {
  it('should update results when user changes filters', () => {
    exploreCards.openResultsPage();

    exploreCards.getNumberResults().then((oldNumResults) => {
      exploreCards.selectCheckboxFilter('rewards', 'Cashback rewards');
      exploreCards.getNumberResults().then((newNumResults) => {
        expect(newNumResults).to.be.lt(oldNumResults);
      });
    });
  });
  it('should show additional results when "Show more" button is clicked', () => {
    exploreCards.openResultsPage();

    exploreCards.getNumberVisibleResults().then((oldNumResults) => {
      exploreCards.clickShowMoreButton();
      exploreCards.getNumberVisibleResults().then((newNumResults) => {
        expect(oldNumResults).to.be.lt(newNumResults);
      });
    });
  });
  it('should link to card detail pages', () => {
    exploreCards.openResultsPage();

    cy.get('td[data-label="Credit card"] a').first().click();

    cy.get('h1').contains('Customize for your situation').should('not.exist');
    cy.get('h2').contains('Application requirements').should('exist');
  });
  it('should have the ordering option outside the filters expandable', () => {
    exploreCards.openResultsPage();

    cy.get('form#tccp-filters select#tccp-ordering').should('not.exist');
  });
});

describe('Explore credit card details page', () => {
  it('should have a breadcrumb to the filtered list the user came from', () => {
    exploreCards.openLandingPage();

    exploreCards.selectCreditTier('Greater than 720');
    exploreCards.selectLocation('NY');
    exploreCards.selectSituation('Earn rewards');
    exploreCards.clickSubmitButton();

    cy.get('td[data-label="Credit card"] a').first().click();

    cy.get('.m-breadcrumbs_crumb:last-child')
      .should('have.attr', 'href')
      .and('contain', 'credit_tier=Credit+score+of+720+or+greater')
      .and('contain', 'location=NY')
      .and('contain', 'situations=Earn+rewards');
  });
  it('should have a breadcrumb to full list if the user never filtered', () => {
    exploreCards.openResultsPage();

    cy.get('td[data-label="Credit card"] a').first().click();

    cy.get('.m-breadcrumbs_crumb:last-child')
      .should('have.attr', 'href')
      .and('eq', '/consumer-tools/credit-cards/explore-cards/cards/');
  });
});
