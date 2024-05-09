import { AskCfpbSearch } from './search-helpers.cy.js';
import { AskCfpbAnswerPage } from './answer-helpers.cy.js';

const search = new AskCfpbSearch();
const answerPage = new AskCfpbAnswerPage();

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

  describe('Answer Page', () => {
    describe('on desktop', () => {
      beforeEach(() => {
        cy.viewport(1200, 800);
        answerPage.open();
      });

      it('should not hide content on desktop', () => {
        answerPage.getFirstLinkInSummary().should('be.visible');
        answerPage.getFirstLinkInSummary().focus();
        answerPage.getFirstLinkInSummary().should('be.visible');
        answerPage.getSummaryBtn().should('not.be.visible');
      });
    });

    describe('on mobile', () => {
      beforeEach(() => {
        answerPage.open();
        cy.viewport(480, 800);
      });

      it('should hide content on mobile', () => {
        cy.get('.o-summary__content').should(
          'have.class',
          'u-max-height-transition',
        );
        cy.get('.o-summary__content').should(
          'have.class',
          'u-max-height-summary',
        );
        cy.get('.o-summary__content')
          .invoke('outerHeight')
          .should('be.lte', 92);
        answerPage.getFirstLinkInSummary().should('not.be.visible');
        answerPage.getSummaryBtn().click();
        answerPage.getFirstLinkInSummary().should('be.visible');
        cy.get('.o-summary__content').should(
          'have.class',
          'u-max-height-transition',
        );
        cy.get('.o-summary__content').should(
          'not.have.class',
          'u-no-animation',
        );
        cy.get('.o-summary__content').should(
          'not.have.class',
          'u-max-height-summary',
        );
        cy.get('.o-summary__content').should(
          'have.class',
          'u-max-height-default',
        );
        cy.get('.o-summary__content').invoke('outerHeight').should('be.gt', 92);
      });
    });
  });
});
