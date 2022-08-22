import { FilingInstructionGuide } from './filing-instruction-guide-helpers.cy.js';
import { skipOn } from '@cypress/skip-test';

const fig = new FilingInstructionGuide();

skipOn( 'staging', () => {

  describe( '1071 Filing Instruction Guide (FIG)', () => {

    describe( 'FIG table of contents', () => {

      /* putting a request in a beforeEach hook will cause the rest of the
         spec to be skipped if the response is not ok. */
      before( () => {
        cy.request( {
          url: '/compliance/compliance-resources/small-business-lending/1071-filing-instruction-guide/',
          failOnStatusCode: true
        } );
      } );

      context( 'Desktop experience', () => {

        const desktops = [
          'macbook-13',
          'macbook-15'
        ];

        desktops.forEach( desktop => {

          context( desktop, () => {

            beforeEach( () => {
              cy.viewport( desktop );
            } );

            it( 'should be present', () => {
              fig.open();
              fig.toc().should( 'be.visible' );
            } );

            it( 'should highlight the first section by default', () => {
              fig.getNavItem( 1 ).should( 'have.class', 'm-nav-link__current' );
              fig.getNavItem( 2 ).should( 'not.have.class', 'm-nav-link__current' );
              fig.getNavItem( 3 ).should( 'not.have.class', 'm-nav-link__current' );
              fig.getNavItem( 4 ).should( 'not.have.class', 'm-nav-link__current' );
            } );

            it( 'should be sticky', () => {
              fig.toc().should( 'be.visible' );
              cy.scrollTo( 0, 1000 );
              // Verify it's still in the viewport after scrolling down the page
              fig.toc().should( 'be.visible' );
              fig.getNavItem( 1 ).should( 'be.visible' );
            } );

            it( 'should be sticky when scrolled to bottom of page', () => {
              fig.toc().should( 'be.visible' );
              fig.scrollToBottom();
              fig.toc().should( 'be.visible' );
            } );

            it( 'should highlight the current section', () => {
              fig.goToSection( 2 );
              fig.getNavItem( 2 ).should( 'have.class', 'm-nav-link__current' );
              fig.getNavItem( 1 ).should( 'not.have.class', 'm-nav-link__current' );
              fig.getNavItem( 3 ).should( 'not.have.class', 'm-nav-link__current' );
              fig.getNavItem( 4 ).should( 'not.have.class', 'm-nav-link__current' );
            } );

            it( 'should auto-expand subsections', () => {
              fig.goToSection( 4.1 );
              fig.getNavItem( 4 ).should( 'be.visible' );
              fig.getNavItem( 4.1 ).should( 'be.visible' );
              fig.getNavItem( 4.2 ).should( 'be.visible' );

              fig.goToSection( 4.2 );
              fig.getNavItem( 4 ).should( 'be.visible' );
              fig.getNavItem( 4.1 ).should( 'be.visible' );
              fig.getNavItem( 4.2 ).should( 'be.visible' );
            } );

            it( 'should auto-close subsections', () => {
              fig.goToSection( 2 );
              fig.getNavItem( 4 ).should( 'be.visible' );
              fig.getNavItem( 4.1 ).should( 'not.be.visible' );
            } );

            it( 'should jump to correct sections', () => {
              fig.clickNavItem( 4 );
              fig.getSection( 4 ).should( 'be.inViewport' );
              fig.getSection( 1 ).should( 'not.be.inViewport' );
              fig.getSection( 2 ).should( 'not.be.inViewport' );
              fig.getSection( 3 ).should( 'not.be.inViewport' );
            } );

            it( 'should highlight correction section when clicking heading', () => {
              fig.clickSectionHeading( 1 );
              fig.getNavItem( 1 ).should( 'have.class', 'm-nav-link__current' );
              fig.getNavItem( 4.1 ).should( 'not.be.visible' );

              fig.clickSectionHeading( 2 );
              fig.getNavItem( 2 ).should( 'have.class', 'm-nav-link__current' );
              fig.getNavItem( 4.1 ).should( 'not.be.visible' );

              fig.clickSectionHeading( 4 );
              fig.getNavItem( 4 ).should( 'have.class', 'm-nav-link__current' );
              fig.getNavItem( 4.1 ).should( 'be.visible' );
            } );

          } );

        } );

      } );

      context( 'Tablet experience', () => {

        const tablets = [
          'ipad-2',
          'ipad-mini'
        ];

        tablets.forEach( tablet => {

          context( tablet, () => {

            beforeEach( () => {
              cy.viewport( tablet );
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

      context( 'Mobile experience', () => {

        const mobiles = [
          'iphone-6',
          'iphone-xr',
          'samsung-note9'
        ];

        mobiles.forEach( mobile => {

          context( mobile, () => {

            beforeEach( () => {
              cy.viewport( mobile );
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

    } );

  } );

} );
