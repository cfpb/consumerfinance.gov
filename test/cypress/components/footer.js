export class Footer {

  footer() {
    return cy.get( '.o-footer' );
  }

  topButton() {
    return this.footer().get( '.o-footer_top-button' );
  }

  navList() {
    return this.footer().get( '.o-footer_nav-list' );
  }

  middle( position ) {
    return this.footer().get( `.o-footer-middle-${ position }` );
  }

  links() {
    return cy.get( '.o-footer_nav-list a, .o-footer-middle-left a,' +
      ' .o-footer-middle-right a, .m-social-media_icons a'
    );
  }

  socialMediaIcons() {
    return this.footer().get( '.m-social-media_icons' );
  }

  officialWebsite() {
    return this.footer().get( '.o-footer-post' );
  }
}
