import { FilingInstructionGuide } from './filing-instruction-guide-helpers.cy.js';
import { onlyOn } from '@cypress/skip-test';

const fig = new FilingInstructionGuide();

describe('1071 Filing Instruction Guide (FIG)', () => {
  describe('FIG table of contents', () => {
    /* Our FIG sample page only exists in certain environments so continue
       this test suite only if the user explicitly provides a URL via
       CYPRESS_FIG_URL=https://blah.cfpb.gov/xxxxxx/yyyyyy/zzzzzz/.
       Once the FIG reaches production we can disable this check. */
    onlyOn(Boolean(fig.url()), () => {
      context('Desktop experience', () => {
        const desktops = ['macbook-13', 'macbook-15'];

        desktops.forEach((desktop) => {
          context(desktop, () => {
            beforeEach(() => {
              cy.viewport(desktop);
            });

            it('should be present', () => {
              fig.open();
              fig.toc().should('be.visible');
            });

            it('should be sticky', () => {
              fig.toc().should('be.visible');
              cy.scrollTo(0, 1000);
              // Verify it's still in the viewport after scrolling down the page
              fig.toc().should('be.visible');
              fig.getNavItem(1).should('be.visible');
            });

            it('should be sticky when scrolled to bottom of page', () => {
              fig.toc().should('be.visible');
              fig.scrollToBottom();
              fig.toc().should('be.visible');
            });

            it('should highlight the current section', () => {
              fig.goToSection(2);
              fig.getNavItem(2).should('have.class', 'm-nav-link__current');
              fig
                .getNavItem(1)
                .should('not.have.class', 'm-nav-link__current');
              fig
                .getNavItem(3)
                .should('not.have.class', 'm-nav-link__current');
              fig
                .getNavItem(4)
                .should('not.have.class', 'm-nav-link__current');
            });

            it('should auto-expand subsections', () => {
              fig.goToSection('credit-type');
              fig.getNavItem(3).should('be.visible');
              fig.getNavItem('credit-type').should('be.visible');
              fig.getNavItem('application-date').should('be.visible');

              fig.goToSection('application-date');
              fig.getNavItem(3).should('be.visible');
              fig.getNavItem('credit-type').should('be.visible');
              fig.getNavItem('application-date').should('be.visible');
            });

            it('should auto-close subsections', () => {
              fig.goToSection(2);
              fig.getNavItem(3).should('be.visible');
              fig.getNavItem('credit-type').should('not.be.visible');
            });

            it('should jump to correct sections', () => {
              fig.clickNavItem(4);
              fig.getSection(4).should('be.inViewport');
              fig.getSection(1).should('not.be.inViewport');
              fig.getSection(2).should('not.be.inViewport');
              fig.getSection(3).should('not.be.inViewport');
            });

            it('should highlight correction section when clicking heading', () => {
              fig.clickSectionHeading(1);
              fig.getNavItem(1).should('have.class', 'm-nav-link__current');
              fig.getNavItem('credit-type').should('not.be.visible');

              fig.clickSectionHeading(3);
              fig.getNavItem(3).should('have.class', 'm-nav-link__current');
              fig.getNavItem('credit-type').should('be.visible');

              fig.clickSectionHeading('application-method');
              fig
                .getNavItem('application-method')
                .should('have.class', 'm-nav-link__current');
              fig.getNavItem('credit-type').should('be.visible');

              fig.clickSectionHeading(5);
              fig.getNavItem(5).should('have.class', 'm-nav-link__current');
              fig.getNavItem('credit-type').should('not.be.visible');

              fig.clickSectionHeading(3);
              fig.getNavItem(3).should('have.class', 'm-nav-link__current');
              fig.getNavItem('credit-type').should('be.visible');

              fig.clickSectionHeading('action-taken');
              fig
                .getNavItem('action-taken')
                .should('have.class', 'm-nav-link__current');
              fig.getNavItem('credit-type').should('be.visible');
            });

            it('should not have any unrendered HTML tags', () => {
              fig.getUnrenderedListTags().should('not.exist');
              fig.getUnrenderedBrTags().should('not.exist');
              fig.getUnrenderedPTags().should('not.exist');
            });
          });
        });
      });

      context('Tablet experience', () => {
        const tablets = ['ipad-2', 'ipad-mini'];

        tablets.forEach((tablet) => {
          context(tablet, () => {
            beforeEach(() => {
              cy.viewport(tablet);
            });

            it('should be present', () => {
              fig.open();
              fig.toc().should('be.visible');
            });

            it('should expand', () => {
              fig.toggleToc();
              fig.getNavItem(1).should('be.visible');
            });

            it('should collapse', () => {
              fig.toggleToc();
              fig.getNavItem(1).should('not.be.visible');
            });

            it('should be sticky', () => {
              fig.toc().should('be.visible');
              cy.scrollTo(0, 1000);
              fig.toc().should('be.visible');
            });

            it('jump to correct sections', () => {
              fig.toggleToc();
              fig.clickNavItem(4);
              fig.getSection(4).should('be.inViewport');
              fig.getSection(2).should('not.be.inViewport');

              fig.toggleToc();
              fig.clickNavItem(1);
              fig.getSection(1).should('be.inViewport');
              fig.getSection(4).should('not.be.inViewport');
            });
          });
        });
      });

      context('Mobile experience', () => {
        const mobiles = ['iphone-6', 'iphone-xr', 'samsung-note9'];

        mobiles.forEach((mobile) => {
          context(mobile, () => {
            beforeEach(() => {
              cy.viewport(mobile);
            });

            it('should be present', () => {
              fig.open();
              fig.toc().should('be.visible');
            });

            it('should expand', () => {
              fig.toggleToc();
              fig.getNavItem(1).should('be.visible');
            });

            it('should collapse', () => {
              fig.toggleToc();
              fig.getNavItem(1).should('not.be.visible');
            });

            it('should be sticky', () => {
              fig.toc().should('be.visible');
              cy.scrollTo(0, 1000);
              fig.toc().should('be.visible');
            });

            it('jump to correct sections', () => {
              fig.toggleToc();
              fig.clickNavItem(4);
              fig.getSection(4).should('be.inViewport');
              fig.getSection(2).should('not.be.inViewport');

              fig.toggleToc();
              fig.clickNavItem(1);
              fig.getSection(1).should('be.inViewport');
              fig.getSection(4).should('not.be.inViewport');
            });
          });
        });
      });
    });
  });
});
