export class Footer {
  footer() {
    return cy.get('.o-footer');
  }

  topButton() {
    return this.footer().get('.o-footer__top-button');
  }

  navList() {
    return this.footer().get('.o-footer__nav-list');
  }

  middle(position) {
    return this.footer().get(`.o-footer-middle-${position}`);
  }

  links() {
    return cy.get(
      '.o-footer__nav-list a, .o-footer-middle-left a,' +
        ' .o-footer-middle-right a, .m-social-media__icons a',
    );
  }

  socialMediaIcons() {
    return this.footer().get('.m-social-media__icons');
  }

  officialWebsite() {
    return this.footer().get('.o-footer-post');
  }
}
