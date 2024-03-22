import { ExploreCreditCards } from './explore-cards-helpers.cy.js';

const exploreCards = new ExploreCreditCards();

describe('Explore credit cards landing page', () => {
  it('should show results tailored to the selected situation', () => {
    exploreCards.openLandingPage();

    exploreCards.selectLocation('FL');
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
});
