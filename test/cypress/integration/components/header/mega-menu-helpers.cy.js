const BASE_CLASS = '.o-mega-menu';

export class MegaMenuDesktop {
  tabs() {
    return cy.get(`${BASE_CLASS}__content-1-link--has-children`);
  }

  firstTab() {
    return this.tabs().first();
  }

  firstTabOpenIcon() {
    return this.firstTab().find(
      `${BASE_CLASS}__content-link-icon-open .cf-icon-svg`,
    );
  }

  firstTabCloseIcon() {
    return this.firstTab().find(
      `${BASE_CLASS}__content-link-icon-closed .cf-icon-svg`,
    );
  }

  secondTab() {
    return this.tabs().eq(1);
  }

  firstPanelContainer() {
    return cy.get(`${BASE_CLASS}__content-2`).first();
  }

  firstPanel() {
    return cy.get(`${BASE_CLASS}__content-2-wrapper`).first();
  }

  secondPanel() {
    return cy.get(`${BASE_CLASS}__content-2-wrapper`).eq(1);
  }
}

export class MegaMenuMobile {
  rootTrigger() {
    return cy.get(`${BASE_CLASS}__trigger`);
  }

  firstLevelTrigger() {
    return cy.get(`${BASE_CLASS}__content-1-link--has-children`).first();
  }

  secondLevelFirstBackTrigger() {
    return cy.get(`${BASE_CLASS}__content-2-alt-trigger`).first();
  }

  firstPanel() {
    return cy.get(`${BASE_CLASS}__content-1`).first();
  }

  secondPanel() {
    return cy.get(`${BASE_CLASS}__content-2`).first();
  }
}
