import { Header } from './header-helpers.cy.js';
import { GlobalSearch } from './global-search-helpers.cy';
import { MegaMenuDesktop, MegaMenuMobile } from './mega-menu-helpers.cy.js';

const header = new Header();
const globalSearch = new GlobalSearch();
const menuDesktop = new MegaMenuDesktop();
const menuMobile = new MegaMenuMobile();

describe('Header', () => {
  describe('on desktop', () => {
    beforeEach(() => {
      cy.viewport(1200, 800);
      cy.visit('/');
    });
    it('clicking from the mega-menu tab to the global search', () => {
      // When I click on the first mega-menu trigger
      menuDesktop.firstTab().click();
      // Then the header organism should display the mega-menu content
      menuDesktop.firstPanel().should('be.visible');
      // When I click on the second mega-menu trigger
      menuDesktop.secondTab().click();
      // Then the header organism should display the mega-menu content
      menuDesktop.secondPanel().should('be.visible');
      // When I click on the global search trigger.
      globalSearch.trigger().click();
      // Then the mega-menu content should not be visible.
      menuDesktop.firstPanel().should('not.be.visible');
      menuDesktop.secondPanel().should('not.be.visible');
    });

    xit('clicking from the global search to the mega-menu', () => {
      // When I click on the global search trigger.
      globalSearch.trigger().click();
      // Then the global search content should be visible.
      globalSearch.content().should('be.visible');
      // When I click on the first mega-menu trigger
      menuDesktop.firstTab().click();
      menuDesktop.firstPanel().should('not.have.class', 'u-is-animating');
      // Scroll to top so global search is visible.
      cy.scrollTo('top');
      // Then the global search content should not be visible.
      globalSearch.content().should('not.be.visible');
      globalSearch.content().should('not.have.class', 'u-is-animating');
    });
    it('on page load', () => {
      // Then the header organism should display the content
      header.headerContent().should('be.visible');
      // And the header organism should display the logo
      header.headerLogo().should('be.visible');
      // And the header organism shouldn't display the overlay
      header.overlay().should('not.be.visible');
      // And should display the global search
      globalSearch.trigger().should('be.visible');
      // And the header organism should display the global eyebrow horizontal
      header.globalEyebrowHorizontal().should('be.visible');
      // And the header organism should display the global header Cta
      header.globalHeaderCta().should('be.visible');
      // And the header organism should display the mega menu content link
      menuDesktop.firstPanel().should('not.be.visible');
    });
  });

  describe('on mobile', () => {
    beforeEach(() => {
      cy.viewport(480, 800);
      cy.visit('/');
    });
    it('clicking from the mega-menu tab to the global search', () => {
      // When I click on the root hamburger menu.
      menuMobile.rootTrigger().click();
      // Then the header organism should display the overlay.
      header.overlay().should('be.visible');
      // Then the header organism should display the mega-menu content.
      menuMobile.firstPanel().should('be.visible');
      // When I click on the global search trigger.
      globalSearch.trigger().click();
      // Then the global search content should be visible.
      globalSearch.content().should('be.visible');
      // Then the mega-menu content should not be visible.
      menuMobile.firstPanel().should('not.be.inViewport');
    });
    xit('clicking from the global search to the mega-menu', () => {
      // When I click on the global search trigger.
      globalSearch.trigger().click();
      // Then the header organism should display the overlay.
      header.overlay().should('be.visible');
      // Then the global search content should be visible.
      globalSearch.content().should('be.visible');
      // When I click on the first mega-menu trigger
      menuMobile.rootTrigger().click();
      menuMobile.firstPanel().should('not.have.class', 'u-is-animating');
      // Then the global search content should not be visible.
      globalSearch.content().should('not.have.class', 'u-is-animating');
      globalSearch.content().should('not.be.visible');
    });
    it('clicking the overlay to close the mega-menu and global search', () => {
      // When I click to the second level mega-menu panel.
      menuMobile.rootTrigger().click();
      menuMobile.firstLevelTrigger().click();
      // When I scroll down the page.
      cy.scrollTo(0, 1500);
      // Then the header organism should display the overlay.
      header.overlay().click();
      // Then the global search content should be visible.
      globalSearch.content().should('not.be.visible');
      // Then the mega-menu content should not be visible.
      menuMobile.firstPanel().should('not.be.inViewport');
      menuMobile.secondPanel().should('not.be.visible');
    });
    it('on page load', () => {
      // Then the header organism should display the content
      header.headerContent().should('be.visible');
      // And the header organism should display the logo
      header.headerLogo().should('be.visible');
      // And the header organism shouldn't display the overlay
      header.overlay().should('not.be.visible');
      // And should display the global search
      globalSearch.trigger().should('be.visible');
      // And the header organism should display the global eyebrow horizontal
      header.globalEyebrowHorizontal().should('be.visible');
      // And the header organism should display the global header Cta
      header.globalHeaderCta().should('not.be.visible');
      // And the header organism should display the mega menu content link
      menuMobile.firstPanel().should('not.be.inViewport');
    });
  });
});
