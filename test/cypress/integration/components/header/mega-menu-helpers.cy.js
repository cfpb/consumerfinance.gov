const BASE_CLASS = '.o-mega-menu';

export class MegaMenuDesktop {
  tabs() {
    return cy.get(`${BASE_CLASS}_content-1-link__has-children`);
  }

  firstTab() {
    return this.tabs().first();
  }

  firstTabOpenIcon() {
    return this.firstTab().find(
      `${BASE_CLASS}_content-link-icon-open .cf-icon-svg`,
    );
  }

  firstTabCloseIcon() {
    return this.firstTab().find(
      `${BASE_CLASS}_content-link-icon-closed .cf-icon-svg`,
    );
  }

  secondTab() {
    return this.tabs().eq(1);
  }

  firstPanelContainer() {
    return cy.get(`${BASE_CLASS}_content-2`).first();
  }

  firstPanel() {
    return cy.get(`${BASE_CLASS}_content-2-wrapper`).first();
  }

  secondPanel() {
    return cy.get(`${BASE_CLASS}_content-2-wrapper`).eq(1);
  }
}

export class MegaMenuMobile {
  rootTrigger() {
    return cy.get(`${BASE_CLASS}_trigger`);
  }

  firstLevelTrigger() {
    return cy.get(`${BASE_CLASS}_content-1-link__has-children`).first();
  }

  secondLevelFirstBackTrigger() {
    return cy.get(`${BASE_CLASS}_content-2-alt-trigger`).first();
  }

  firstPanel() {
    return cy.get(`${BASE_CLASS}_content-1`).first();
  }

  secondPanel() {
    return cy.get(`${BASE_CLASS}_content-2`).first();
  }
}
