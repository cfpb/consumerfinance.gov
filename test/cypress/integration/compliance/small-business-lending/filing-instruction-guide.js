import { FilingInstructionGuide } from './filing-instruction-guide-helpers';

const fig = new FilingInstructionGuide();

describe( '1071 Filing Instruction Guide (FIG)', () => {

  describe( 'FIG table of contents', () => {

    context( 'Desktop experience', () => {

      beforeEach( () => {
        cy.viewport( 'macbook-13' );
      } );

      it( 'should be present', () => {
        fig.open();
        fig.toc().should( 'be.visible' );
      } );

      it( 'should highlight the first section by default', () => {
        fig.getNavItem( 1 ).should( 'have.class', 'm-nav-link__current' );
      } );

      it( 'should be sticky', () => {
        fig.toc().should( 'be.visible' );
        cy.scrollTo( 0, 1000 );
        // Verify it's still in the viewport after scrolling down the page
        fig.toc().should( 'be.visible' );
      } );

      it( 'should highlight the current section', () => {
        fig.goToSection( 2 );
        fig.getNavItem( 2 ).should( 'have.class', 'm-nav-link__current' );
      } );

      it( 'should auto-expand subsections', () => {
        fig.goToSection( 4.1 );
        fig.getNavItem( 4 ).should( 'be.visible' );
        fig.getNavItem( 4.1 ).should( 'be.visible' );
      } );

      it( 'should auto-close subsections', () => {
        fig.goToSection( 2 );
        fig.getNavItem( 4 ).should( 'be.visible' );
        fig.getNavItem( 4.1 ).should( 'not.be.visible' );
      } );

      it( 'jump to correct sections', () => {
        fig.clickNavItem( 4 );
        fig.getSection( 4 ).should( 'be.inViewport' );
        fig.getSection( 2 ).should( 'not.be.inViewport' );
      } );

      it( 'highlight correction section when clicking heading', () => {
        fig.clickSectionHeading( 1 );
        fig.getNavItem( 1 ).should( 'have.class', 'm-nav-link__current' );
        fig.getNavItem( 4.1 ).should( 'not.be.visible' );
      } );

    } );

    context( 'Tablet experience', () => {

      beforeEach( () => {
        cy.viewport( 'ipad-2' );
      } );

      it( 'should be present', () => {
        fig.open();
        fig.toc().should( 'be.visible' );
      } );

      it( 'should expand', () => {
        fig.toggleToc();
        fig.getNavItem( 1 ).should( 'be.visible' );
      } );

      it( 'should collapse', () => {
        fig.toggleToc();
        fig.getNavItem( 1 ).should( 'not.be.visible' );
      } );

      it( 'should be sticky', () => {
        fig.toc().should( 'be.visible' );
        cy.scrollTo( 0, 1000 );
        // Verify it's still in the viewport after scrolling down the page
        fig.toc().should( 'be.visible' );
      } );

      it( 'jump to correct sections', () => {
        fig.toggleToc();
        fig.clickNavItem( 4 );
        fig.getSection( 4 ).should( 'be.inViewport' );
        fig.getSection( 2 ).should( 'not.be.inViewport' );

        fig.toggleToc();
        fig.clickNavItem( 1 );
        fig.getSection( 1 ).should( 'be.inViewport' );
        fig.getSection( 4 ).should( 'not.be.inViewport' );
      } );

    } );

    context( 'Mobile experience', () => {

      beforeEach( () => {
        cy.viewport( 'iphone-xr' );
      } );

      it( 'should be present', () => {
        fig.open();
        fig.toc().should( 'be.visible' );
      } );

      it( 'should expand', () => {
        fig.toggleToc();
        fig.getNavItem( 1 ).should( 'be.visible' );
      } );

      it( 'should collapse', () => {
        fig.toggleToc();
        fig.getNavItem( 1 ).should( 'not.be.visible' );
      } );

      it( 'should be sticky', () => {
        fig.toc().should( 'be.visible' );
        cy.scrollTo( 0, 1000 );
        // Verify it's still in the viewport after scrolling down the page
        fig.toc().should( 'be.visible' );
      } );

      it( 'jump to correct sections', () => {
        fig.toggleToc();
        fig.clickNavItem( 4 );
        fig.getSection( 4 ).should( 'be.inViewport' );
        fig.getSection( 2 ).should( 'not.be.inViewport' );

        fig.toggleToc();
        fig.clickNavItem( 1 );
        fig.getSection( 1 ).should( 'be.inViewport' );
        fig.getSection( 4 ).should( 'not.be.inViewport' );
      } );

    } );

  } );

} );
