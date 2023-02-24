import { MegaMenuDesktop, MegaMenuMobile } from './mega-menu-helpers.cy.js';

const menuDesktop = new MegaMenuDesktop();
const menuMobile = new MegaMenuMobile();

describe('Mega-Menu organism for site navigation', () => {
  describe('on desktop', () => {
    beforeEach(() => {
      cy.visit('/');
      cy.viewport(1200, 800);
    });
    it('on page load', () => {
      // Then the mega-menu organism should not have expanded attributes.
      menuDesktop.firstTab().should('have.attr', 'aria-expanded', 'false');
      menuDesktop
        .firstPanelContainer()
        .should('have.attr', 'aria-expanded', 'false');
      // Then the mega-menu organism should have correct CSS classes.
      menuDesktop.firstPanel().should('have.class', 'u-move-transition');
      menuDesktop.firstPanel().should('have.class', 'u-move-up');
      menuDesktop.firstPanel().should('not.have.class', 'u-is-animating');
      // Then the mega-menu organism panels should not be visible.
      menuDesktop.firstPanel().should('not.be.visible');
      menuDesktop.secondPanel().should('not.be.visible');
    });
    it('on clicking a tab', () => {
      // When the first tab is clicked to open.
      menuDesktop.firstTab().click();
      // Then the mega-menu organism should have expanded attributes.
      menuDesktop.firstTab().should('have.attr', 'aria-expanded', 'true');
      menuDesktop
        .firstPanelContainer()
        .should('have.attr', 'aria-expanded', 'true');
      // Then the mega-menu organism should have correct CSS classes.
      menuDesktop.firstPanel().should('have.class', 'u-move-transition');
      menuDesktop.firstPanel().should('have.class', 'u-move-to-origin');
      menuDesktop.firstPanel().should('not.have.class', 'u-is-animating');
      // Then the mega-menu organism panels should be correctly displayed.
      menuDesktop.firstPanel().should('be.visible');
      menuDesktop.secondPanel().should('not.be.visible');
      // When the first tab is clicked to close.
      menuDesktop.firstTab().click();
      // Then the mega-menu organism first panel should not be visible.
      menuDesktop.firstPanel().should('not.be.visible');
      // Then the mega-menu organism should have correct CSS classes.
      menuDesktop.firstPanel().should('have.class', 'u-move-transition');
      menuDesktop.firstPanel().should('have.class', 'u-move-up');
      menuDesktop.firstPanel().should('not.have.class', 'u-is-animating');
      // When the second tab is clicked to open.
      menuDesktop.secondTab().click();
      // Then the mega-menu organism should have correct CSS classes.
      menuDesktop.secondPanel().should('have.class', 'u-move-transition');
      menuDesktop.secondPanel().should('have.class', 'u-move-to-origin');
      menuDesktop.secondPanel().should('not.have.class', 'u-is-animating');
      // Then the mega-menu organism panels should be correctly displayed.
      menuDesktop.firstPanel().should('not.be.visible');
      menuDesktop.secondPanel().should('be.visible');
    });
    it('on clicking between tabs', () => {
      // When the first tab is clicked to open.
      menuDesktop.firstTab().click();
      // Then only the first panel should be visible.
      menuDesktop.firstPanel().should('be.visible');
      menuDesktop.secondPanel().should('not.be.visible');
      // When the second tab is clicked to open.
      menuDesktop.secondTab().click();
      // Then only the second panel should be visible.
      menuDesktop.firstPanel().should('not.be.visible');
      menuDesktop.secondPanel().should('be.visible');
    });
  });

  describe('on mobile', () => {
    beforeEach(() => {
      cy.viewport(480, 800);
      cy.visit('/');
    });
    it('on page load', () => {
      // Then the mega-menu organism should not have expanded attributes.
      menuMobile.rootTrigger().should('have.attr', 'aria-expanded', 'false');
      menuMobile.firstPanel().should('have.attr', 'aria-expanded', 'false');
      menuMobile.firstLevelTrigger().should('have.attr', 'tabindex', '-1');
      menuMobile.firstLevelTrigger().should('have.attr', 'aria-hidden', 'true');
      // Then the mega-menu organism should have correct CSS classes.
      menuMobile.firstPanel().should('have.class', 'u-move-transition');
      menuMobile.firstPanel().should('have.class', 'u-move-left');
      menuMobile.firstPanel().should('not.have.class', 'u-is-animating');
      // Then the mega-menu organism panels should not be visible.
      menuMobile.firstPanel().should('not.be.inViewport');
      menuMobile.secondPanel().should('not.be.visible');
    });
    it('on drilling down to the second level and back', () => {
      // When the hamburger menu is clicked to open.
      menuMobile.rootTrigger().click();
      // Then only the first panel should be visible.
      menuMobile.firstPanel().should('be.visible');
      menuMobile.secondPanel().should('not.be.visible');
      menuMobile.firstLevelTrigger().should('not.have.attr', 'tabindex');
      menuMobile.firstLevelTrigger().should('not.have.attr', 'aria-hidden');
      // Then expected content is visible.
      menuMobile.firstPanel().contains('Submit a Complaint');
      menuMobile.firstPanel().contains('Español');
      menuMobile.firstPanel().contains('(855) 411-2372');
      // When the first child menu is clicked.
      menuMobile.firstLevelTrigger().click();
      // Then only the second panel should be visible.
      menuMobile.firstPanel().should('not.be.inViewport');
      menuMobile.secondPanel().should('be.visible');
      // When the second panel's back button is clicked.
      menuMobile.secondLevelFirstBackTrigger().should('be.focused');
      menuMobile.secondLevelFirstBackTrigger().click();
      // Then only the first panel should be visible.
      menuMobile.firstPanel().should('be.visible');
      menuMobile.secondPanel().should('not.be.visible');
    });
    it('on opening and closing the menu', () => {
      // When the hamburger menu is clicked to open and then to close.
      menuMobile.rootTrigger().click();
      menuMobile.rootTrigger().click();
      // Then the mega-menu organism panels should not be visible.
      menuMobile.firstPanel().should('not.be.inViewport');
      menuMobile.secondPanel().should('not.be.visible');
      // When the hamburger menu is clicked to open.
      menuMobile.rootTrigger().click();
      // When the first child menu is clicked.
      menuMobile.firstLevelTrigger().click();
      // When the hamburger menu is clicked to close.
      menuMobile.rootTrigger().click();
      // Then the mega-menu organism panels should not be visible.
      menuMobile.firstPanel().should('not.be.inViewport');
      menuMobile.secondPanel().should('not.be.visible');
    });

    xit('on tabbing interactions', () => {
      // TODO: Cypress does not currently support tabbing keyboard interactions.
      // See https://github.com/cypress-io/cypress/issues/299
    });
  });
});
