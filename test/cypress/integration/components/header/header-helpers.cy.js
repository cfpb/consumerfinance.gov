export class Header {
  headerContent() {
    return cy.get('.o-header_content');
  }

  headerLogo() {
    return cy.get('.o-header_logo-img');
  }

  /* Overlay is technically outside of the header,
     but makes organizational sense to include here. */
  overlay() {
    return cy.get('.a-overlay');
  }

  globalHeaderElement(name) {
    return cy.get(`.m-global-header-${name}`);
  }

  globalHeaderCta() {
    return this.globalHeaderElement('cta');
  }

  globalEyebrowHorizontal() {
    return cy.get('.m-global-eyebrow__horizontal');
  }
}
