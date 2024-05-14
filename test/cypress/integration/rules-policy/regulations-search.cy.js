import { RegulationsSearch } from './regulations-search-helpers.cy.js';

const regulationsSearch = new RegulationsSearch();

describe('Policy Compliance', () => {
  describe('Regulations Search', () => {
    beforeEach(() => {
      regulationsSearch.open();
      regulationsSearch.searchTerm('mortgage');
    });

    it('should return results based on search term', () => {
      regulationsSearch.searchResults().should('be.visible');
    });

    it('should allow clearing of search', () => {
      regulationsSearch.input().type('typed a typoo');
      regulationsSearch.resetButton().should('be.visible');
      regulationsSearch.clearSearch();
      regulationsSearch.input().invoke('val').should('be.empty');
      regulationsSearch.resetButton().should('not.be.visible');
    });

    it('should adjust results based on the page size', () => {
      regulationsSearch.setPageSize(50);
      regulationsSearch.searchResult().should('have.length', '50');
    });

    it('should limit results based on regulation', () => {
      regulationsSearch.selectRegulation(1008);
      regulationsSearch.filters().should('be.visible');
      regulationsSearch.filters().should('contain', 1008);
    });
  });
});
