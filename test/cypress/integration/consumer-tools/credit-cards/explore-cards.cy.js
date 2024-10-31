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
    exploreCards.checkA11y();
  });

  it("should show an error message if a location isn't selected", () => {
    exploreCards.openLandingPage();

    cy.get('.a-form-alert__text').should('not.be.visible');

    exploreCards.selectSituation('Earn rewards');
    exploreCards.clickSubmitButton();

    cy.get('.a-form-alert__text').should('be.visible');
    exploreCards.checkA11y();

    exploreCards.selectLocation('NY');

    cy.get('.a-form-alert__text').should('not.be.visible');
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
  it('should not follow card links when tooltips are clicked', () => {
    exploreCards.openResultsPage();

    cy.get('.m-card--tabular [data-tooltip]').first().trigger('mouseenter');

    cy.get('h1').contains('Explore credit cards').should('exist');
    cy.get('h2')
      .contains('Purchase interest rate and fees')
      .should('not.exist');
  });
  it('should close tooltips when escape key is pressed', () => {
    exploreCards.openResultsPage();

    cy.get('.m-card--tabular [data-tooltip]').first().trigger('mouseenter');
    cy.get('div.tippy-heading').should('be.visible');

    cy.get('.m-card--tabular [data-tooltip]').first().type('{esc}');
    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000);
    cy.get('div.tippy-heading').should('not.exist');
  });
  it('should not follow card links when tooltips are open', () => {
    exploreCards.openResultsPage();

    // Open a tooltip
    cy.get('.m-card--tabular [data-tooltip]').first().click();
    // Click away to close the tooltip
    cy.get('.m-card--tabular .m-card__heading-group').first().click();

    // The link should not have been followed
    cy.get('h1').contains('Explore credit cards').should('exist');
    cy.get('h2')
      .contains('Purchase interest rate and fees')
      .should('not.exist');

    // eslint-disable-next-line cypress/no-unnecessary-waiting
    cy.wait(1000);
    // Click a second time now that the tooltip is closed
    cy.get('.m-card--tabular .m-card__heading-group').first().click();
    // The link should now have been followed
    cy.get('h1').contains('Explore credit cards').should('not.exist');
    cy.get('h2').contains('Purchase interest rate and fees').should('exist');
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
  it('should only show the "Show more" button when not ordering by product name', () => {
    exploreCards.openResultsPage('ordering=product_name');
    exploreCards.getOrderingDropdownValue().should('have.text', 'Card name');
    cy.get('#u-show-more-fade').should('not.be.visible');

    exploreCards.selectOrdering('Purchase APR');
    cy.get('.htmx-container.htmx-request').should('not.exist');
    cy.get('#u-show-more-fade').should('be.visible');
    exploreCards.checkA11y();

    exploreCards.selectOrdering('Card name');
    cy.get('.htmx-container.htmx-request').should('not.exist');
    cy.get('#u-show-more-fade').should('not.be.visible');

    exploreCards.selectOrdering('Purchase APR');
    cy.get('.htmx-container.htmx-request').should('not.exist');
    cy.get('#u-show-more-fade').should('be.visible');
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
  it('should have an aria-busy=true attribute when an AJAX request is in-flight', () => {
    exploreCards.openResultsPage('situations=Build%20credit');
    cy.get('#htmx-results[aria-busy=true]').should('not.exist');

    exploreCards.selectCheckboxFilter('rewards', 'Cashback rewards');
    cy.get('#htmx-results[aria-busy=true]').should('exist');
  });
  it('should link to card detail pages', () => {
    exploreCards.openResultsPage();

    cy.get('.m-card--tabular > a').first().click();

    cy.get('h1').contains('Explore credit cards').should('not.exist');
    cy.get('h2').contains('Purchase interest rate and fees').should('exist');
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

    cy.get('.m-breadcrumbs__crumb:last-child')
      .should('have.attr', 'href')
      .and('contain', 'credit_tier=Credit+score+of+720+or+greater')
      .and('contain', 'location=NY')
      .and('contain', 'situations=Earn+rewards');
    exploreCards.checkA11y();
  });
  it('should have a breadcrumb to full list if the user never filtered', () => {
    exploreCards.openResultsPage();

    cy.get('.m-card--tabular > a').first().click();

    cy.get('.m-breadcrumbs__crumb:last-child')
      .should('have.attr', 'href')
      .and('eq', '/consumer-tools/credit-cards/explore-cards/cards/');
  });
});
