import { AskCfpbSearch } from './search-helpers.cy.js';

const search = new AskCfpbSearch();

describe('Ask CFPB', () => {
  describe('Search', () => {
    beforeEach(() => {
      search.open('en');
    });

    it('should autocomplete results', () => {
      search.enter('security');
      search.autocomplete().should('be.visible');
    });

    it('should return results', () => {
      search.enter('security');
      search.search();
      search.resultsSection().should('be.visible');
    });

    it('should correct spelling', () => {
      search.enter('vehile');
      search.search();
      search.resultsHeader().should('contain', 'results for “vehicle”');
      search
        .resultsHeader()
        .siblings('p')
        .first()
        .should('contain', 'Search instead for');
    });

    it('should limit queries to a maximum length', () => {
      search.enter(search.longTerm());
      search
        .input()
        .should('contain.class', 'a-text-input--error')
        .and('have.attr', 'maxlength');
      search.maxLengthErrorMessage().should('be.visible');
      search.submitButton().should('be.disabled');
    });

    it('should allow clearing of search', () => {
      search.enter('typed a typoo');
      search.resetButton().should('be.visible');
      search.clearSearch();
      search.input().invoke('val').should('be.empty');
      search.resetButton().should('not.be.visible');
    });
  });
});
