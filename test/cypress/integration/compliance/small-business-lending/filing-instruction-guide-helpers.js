export class FilingInstructionGuide {

  open() {
    cy.visit( '/compliance/compliance-resources/small-business-lending/1071-filing-instruction-guide/' );
  }

  toc() {
    return cy.get( '.o-fig .content_sidebar' );
  }

  getSection( section ) {
    return cy.get( `a[id="${ section }"]` );
  }

  goToSection( section ) {
    return this.getSection( section ).scrollIntoView( { duration: 1000 } );
  }

  getNavItem( section ) {
    return cy.get( `a.m-nav-link[href="#${ section }"]` );
  }

  clickNavItem( section ) {
    return this.getNavItem( section ).click();
  }

  clickSectionHeading( section ) {
    return this.getSection( section ).click();
  }

  expectSectionInViewport( section ) {
    return this.getSection( section ).isWithinViewport();
  }

  expectSectionNotInViewport( section ) {
    return this.getSection( section ).isNotWithinViewport();
  }

  toggleToc() {
    return cy.get( '.o-expandable_header' ).click();
  }

  scrollToBottom() {
    return cy.get( 'footer' ).scrollIntoView( { duration: 1000 } );
  }

}
