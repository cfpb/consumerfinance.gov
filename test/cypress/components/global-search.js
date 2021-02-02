export class GlobalSearch {

  globalSearch( name ) {
    return cy.get( `.m-global-search ${ name }` );
  }

  globalSearchMenu( name ) {
    return this.globalSearch( `[data-js-hook="behavior_flyout-menu_${ name }"]` );
  }

  footerTagline() {
    return cy.get( '.o-footer .a-tagline' );
  }

  trigger() {
    return this.globalSearchMenu( 'trigger' );
  }

  content() {
    return this.globalSearchMenu( 'content' );
  }

  input() {
    return this.globalSearch( 'input#m-global-search_query' );
  }

  button() {
    return this.globalSearch( '[data-js-hook="behavior_flyout-menu_content"] .a-btn' );
  }

  suggest() {
    return this.globalSearch( '.m-global-search_content-suggestions' );
  }
}
