export class Header {

  headerContent() {
    return cy.get( '.o-header_content' );
  }

  headerLogo() {
    return cy.get( '.o-header_logo-img' );
  }

  /* Overlay is technically outside of the header,
    but makes organizational sense to include here. */
  overlay() {
    return cy.get( '.a-overlay' );
  }

  globalHeaderElement( name ) {
    return cy.get( `.m-global-header-${ name }` );
  }

  globalSearchElement( name ) {
    return cy.get( `.m-global-search_${ name }` );
  }

  globalSearch() {
    return cy.get( '.m-global-search' );
  }

  globalSearchTrigger() {
    return this.globalSearchElement( 'trigger' );
  }

  globalSearchContent() {
    return this.globalSearchElement( 'content' );
  }

  globalHeaderCta() {
    return this.globalHeaderElement( 'cta' );
  }

  megaMenuHeader() {
    return cy.get( '.o-header__o-mega-menu' );
  }
}
