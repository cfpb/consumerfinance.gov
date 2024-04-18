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
      expect(oldNumResults).to.eq(10);
      exploreCards.clickShowMoreButton();
      exploreCards.getNumberVisibleResults().then((newNumResults) => {
        expect(oldNumResults).to.be.lt(newNumResults);
      });
    });
  });
  it('should show speed bumps when situation(s) are selected', () => {
    exploreCards.openResultsPage('situations=Build%20credit');
    exploreCards.getNumberVisibleSpeedBumps().then((numSpeedBumps) => {
      expect(numSpeedBumps).to.eq(1);
    });

    exploreCards.openResultsPage(
      'situations=Make%20a%20big%20purchase&situations=Build%20credit',
    );
    exploreCards.getNumberVisibleSpeedBumps().then((numSpeedBumps) => {
      expect(numSpeedBumps).to.eq(2);
      exploreCards.clickShowMoreButton();
      exploreCards.getNumberVisibleSpeedBumps().then((numSpeedBumps) => {
        expect(numSpeedBumps).to.be.gt(2);
      });
    });
  });
  it('should link to card detail pages', () => {
    exploreCards.openResultsPage();

    cy.get('.m-card--tabular > a').first().click();

    cy.get('h1').contains('Explore credit cards').should('not.exist');
    cy.get('h2').contains('Making purchases').should('exist');
  });
  it('should have the ordering option outside the filters expandable', () => {
    exploreCards.openResultsPage();

    cy.get('form#tccp-filters select#tccp-ordering').should('not.exist');
    exploreCards.getOrderingDropdownValue().should('have.text', 'Purchase APR');
    exploreCards.selectOrdering('Card name');
    exploreCards.getOrderingDropdownValue().should('have.text', 'Card name');
  });
});

describe('Explore credit card details page', () => {
  it('should have a breadcrumb to the filtered list the user came from', () => {
    exploreCards.openLandingPage();

    exploreCards.selectCreditTier('720 and greater');
    exploreCards.selectLocation('NY');
    exploreCards.selectSituation('Earn rewards');
    exploreCards.clickSubmitButton();

    cy.get('.m-card--tabular > a').first().click();

    cy.get('.m-breadcrumbs_crumb:last-child')
      .should('have.attr', 'href')
      .and('contain', 'credit_tier=Credit+score+of+720+or+greater')
      .and('contain', 'location=NY')
      .and('contain', 'situations=Earn+rewards');
  });
  it('should have a breadcrumb to full list if the user never filtered', () => {
    exploreCards.openResultsPage();

    cy.get('.m-card--tabular > a').first().click();

    cy.get('.m-breadcrumbs_crumb:last-child')
      .should('have.attr', 'href')
      .and('eq', '/consumer-tools/credit-cards/explore-cards/cards/');
  });
});
