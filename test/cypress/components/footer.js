export class Footer {

  open( url ) {
    cy.visit( url || '/' );
  }

  footer() {
    return cy.get( '.o-footer' );
  }

  navList() {
    return this.footer().get( '.o-footer_nav-list' );
  }

  links() {
    return cy.get( '.o-footer_nav-list a, .o-footer-middle-left a,' +
      ' .o-footer-middle-right a, .o-footer_share-icon-list a'
    );
  }

  post() {
    return this.footer().get( '.o-footer-post' );
  }

  shareIconList() {
    return this.footer().get( '.o-footer_share-icon-list' );
  }

  officialWebsite() {
    return this.footer().get( '.o-footer_official-website' );
  }
};
