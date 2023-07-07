import { FilingInstructionGuide } from './filing-instruction-guide-helpers.cy.js';

const fig = new FilingInstructionGuide();

const deviceAgnosticSpecs = () => {
  it('should not open the search modal on page load', () => {
    fig.open();
    fig.getSearchModal().should('not.be.visible');
  });

  it('should open the search modal when query param exists', () => {
    cy.visit(fig.url() + '?search=true');
    fig.getSearchModal().should('be.visible');
  });

  it('should close the search modal when the bg overlay is clicked', () => {
    cy.visit(fig.url() + '?search=true');
    fig.getSearchModal().click(5, 5);
    fig.getSearchModal().should('not.be.visible');
  });

  it('should close the search modal when the esc key is pressed', () => {
    cy.visit(fig.url() + '?search=true');
    fig.getSearchModal().should('be.visible');
    fig.getSearchInput().type('{esc}');
    fig.getSearchModal().should('not.be.visible');
  });

  it('should close when the close button is clicked', () => {
    cy.visit(fig.url() + '?search=true');
    fig.getSearchModal().should('be.visible');
    fig.getSearchModalCloseButton().trigger('click');
    fig.getSearchModal().should('not.be.visible');
  });

  it('should show search results', () => {
    cy.visit(fig.url() + '?search=true');
    fig.getSearchResults().should('not.be.visible');
    fig.getSearchInput().type('filing');
    fig.getSearchResults().should('be.visible');
  });

  it('should clear search results and the search input when the clear button is clicked', () => {
    cy.visit(fig.url() + '?search=true');
    fig.getSearchResults().should('not.be.visible');
    fig.getSearchInput().type('filing');
    fig.getSearchResults().should('be.visible');
    fig.getSearchInputClearButton().trigger('click');
    fig.getSearchResults().should('not.be.visible');
    fig.getSearchInput().invoke('val').should('be.empty');
  });

  it('should have keyboard-navigable search results', () => {
    cy.visit(fig.url() + '?search=true');
    fig.getSearchInput().type('filing');
    // The search input has a 300ms debounce so wait for results to show
    // before hitting the downArrow key twice
    fig.getSearchResults().should('be.visible');
    fig.getSearchInput().type('{downArrow}{downArrow}');
    cy.focused().parent().should('have.class', 'ctrl-f-search-result');
  });

  it('should close after following a result', () => {
    cy.visit(fig.url() + '?search=true');
    fig.getSearchInput().type('filing');
    fig.getSearchResults().should('be.visible');
    fig.getFirstSearchResult().trigger('click');
    fig.getSearchResults().should('not.be.visible');
  });
};

describe('1071 Filing Instruction Guide (FIG)', () => {
  describe('FIG search feature', () => {
    context('Desktop experience', () => {
      const desktops = ['macbook-13', 'macbook-15'];

      desktops.forEach((desktop) => {
        context(desktop, () => {
          beforeEach(() => {
            cy.viewport(desktop);
          });

          deviceAgnosticSpecs();

          it('should open the search modal when the search input is clicked', () => {
            fig.open();
            fig.getSearchButton().trigger('click');
            fig.getSearchModal().should('be.visible');
          });
        });
      });
    });

    context('Tablet experience', () => {
      const tablets = ['ipad-2', 'ipad-mini'];
      const orientations = ['portrait', 'landscape'];

      tablets.forEach((tablet) => {
        orientations.forEach((orientation) => {
          context(`${tablet} in ${orientation} mode`, () => {
            beforeEach(() => {
              cy.viewport(tablet, orientation);
            });

            deviceAgnosticSpecs();
          });
        });
      });
    });

    context('Mobile experience', () => {
      const mobiles = ['iphone-6', 'iphone-xr', 'samsung-note9'];
      const orientations = ['portrait', 'landscape'];

      mobiles.forEach((mobile) => {
        orientations.forEach((orientation) => {
          context(`${mobile} in ${orientation} mode`, () => {
            beforeEach(() => {
              cy.viewport(mobile, orientation);
            });

            deviceAgnosticSpecs();

            it('should open the search modal when the search input is clicked', () => {
              fig.open();
              fig.toggleToc();
              fig.getSearchButton().trigger('click');
              fig.getSearchModal().should('be.visible');
            });

            it('should close the TOC after following a result', () => {
              cy.visit(fig.url() + '?search=true');
              fig.getSearchInput().type('filing');
              fig.getFirstSearchResult().trigger('click');
              fig.getMobileTOCBody().should('not.be.visible');
            });
          });
        });
      });
    });
  });
});
