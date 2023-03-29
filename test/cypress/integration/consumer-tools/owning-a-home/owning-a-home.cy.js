import { ExploreRates } from './explore-rates-helpers.cy.js';

const exploreRates = new ExploreRates();

describe('Owning a Home', () => {
  describe('Explore Rates', () => {
    beforeEach(() => {
      cy.visit('/owning-a-home/explore-rates/');
    });
    it('Should load the interest rates graph when a state has changed', () => {
      exploreRates.selectState('Virginia');
      exploreRates.getGraph().should('exist');
    });

    it('Should display high balance FHA loan when house price is high', () => {
      exploreRates.getHousePriceInput().type('400000');
      exploreRates.getCountySelector().should('not.be.visible');
      exploreRates.getCountyAlert().should('not.be.visible');
      exploreRates
        .getLoanTypeSelector()
        .get('[value="fha-hb"]')
        .should('not.exist');
      exploreRates.getHighBalanceAlert().should('not.be.visible');

      exploreRates.selectLoanType('fha');
      exploreRates.getCountySelector().should('be.visible');
      exploreRates.getCountyAlert().should('be.visible');
      exploreRates.selectCounty('Baldwin');
      exploreRates.getLoanTypeSelector().get('[value="conf"]').should('exist');
      exploreRates.getLoanTypeSelector().get('[value="fha"]').should('exist');
      exploreRates.getLoanTypeSelector().get('[value="va"]').should('exist');
      exploreRates
        .getLoanTypeSelector()
        .get('[value="fha-hb"]')
        .should('exist');
      exploreRates.getHighBalanceAlert().should('be.visible');
    });

    it('Should display high balance VA loan when house price is high', () => {
      exploreRates.getHousePriceInput().type('600000');
      exploreRates.getCountySelector().should('be.visible');
      exploreRates.getCountyAlert().should('be.visible');
      exploreRates
        .getLoanTypeSelector()
        .get('[value="va-hb"]')
        .should('not.exist');
      exploreRates.getHighBalanceAlert().should('not.be.visible');

      exploreRates.selectLoanType('va');
      exploreRates.selectCounty('Baldwin');
      exploreRates.getLoanTypeSelector().get('[value="conf"]').should('exist');
      exploreRates.getLoanTypeSelector().get('[value="fha"]').should('exist');
      exploreRates.getLoanTypeSelector().get('[value="va"]').should('exist');
      exploreRates.getLoanTypeSelector().get('[value="va-hb"]').should('exist');
      exploreRates.getHighBalanceAlert().should('be.visible');
    });

    it('Should display conforming jumbo loan type when house price is very high', () => {
      exploreRates.getHousePriceInput().type('700000');
      exploreRates.getCountySelector().should('be.visible');
      exploreRates.getCountyAlert().should('be.visible');
      exploreRates
        .getLoanTypeSelector()
        .get('[value="agency"]')
        .should('not.exist');
      exploreRates.getHighBalanceAlert().should('not.be.visible');
      exploreRates.selectCounty('Baldwin');
      exploreRates
        .getLoanTypeSelector()
        .get('[value="agency"]')
        .should('exist');
      exploreRates.getHighBalanceAlert().should('be.visible');
    });

    it('Should display non-conforming jumbo loan type when house price is very very high', () => {
      exploreRates.getHousePriceInput().type('1000000');
      exploreRates.getCountySelector().should('be.visible');
      exploreRates.getCountyAlert().should('be.visible');
      exploreRates
        .getLoanTypeSelector()
        .get('[value="jumbo"]')
        .should('not.exist');
      exploreRates.getHighBalanceAlert().should('not.be.visible');
      exploreRates.selectCounty('Baldwin');
      exploreRates.getLoanTypeSelector().get('[value="jumbo"]').should('exist');
      exploreRates.getHighBalanceAlert().should('be.visible');
    });

    it('Should display ARM type selector when rate type is adjustable', () => {
      exploreRates.getChartResultAlert().should('not.be.visible');
      exploreRates.getArmTypeSelector().should('not.be.visible');
      exploreRates.selectRateType('Adjustable');
      exploreRates.getChartResultAlert().should('be.visible');
      exploreRates.getArmTypeSelector().should('be.visible');
      exploreRates
        .getLoanTermSelector()
        .get('[value="30"]')
        .should('not.be.disabled');
      exploreRates
        .getLoanTermSelector()
        .get('[value="15"]')
        .should('be.disabled');
      exploreRates
        .getLoanTypeSelector()
        .get('[value="conf"]')
        .should('not.be.disabled');
      exploreRates
        .getLoanTypeSelector()
        .get('[value="fha"]')
        .should('be.disabled');
      exploreRates
        .getLoanTypeSelector()
        .get('[value="va"]')
        .should('be.disabled');
    });
  });
});
