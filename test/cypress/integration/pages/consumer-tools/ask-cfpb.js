import { AskCfpbSearch } from '../../../pages/consumer-tools/ask-cfpb/search';
import { AskCfpbAnswerPage } from '../../../pages/consumer-tools/ask-cfpb/answer-page';

const search = new AskCfpbSearch();
const answerPage = new AskCfpbAnswerPage();

describe( 'Ask CFPB', () => {
  describe( 'Search', () => {
    beforeEach( () => {
      search.open();
    } );

    it( 'should autocomplete results', () => {
      search.enter( 'security' );
      search.autocomplete().should( 'be.visible' );
    } );

    it( 'should return results', () => {
      search.enter( 'security' );
      search.search();
      search.resultsSection().should( 'be.visible' );
    } );

    it( 'should correct spelling', () => {
      search.enter( 'vehile' );
      search.search();
      search.resultsHeader().should( 'contain', 'results for “vehicle”' );
      search.resultsHeader().siblings( 'p' ).first().should( 'contain', 'Search instead for' );
    } );

    it( 'should limit queries to a maximum length', () => {
      const maxLength = Cypress.$( '#o-search-bar_query' ).attr( 'maxlength' );
      const longTerm = new Array( parseInt( maxLength, 10 ) + 1 ).join( 'c' );
      search.enter( longTerm );
      search.input().should( 'contain.class', 'a-text-input__error' )
        .and( 'have.attr', 'maxlength' );
      search.maxLengthErrorMessage().should( 'be.visible' );
    } );
  } );

  describe( 'Answer Page', () => {
    beforeEach( () => {
      answerPage.open();
    } );

    it( 'should hide content on mobile', () => {
      cy.viewport( 600, 1000 );
      cy.get( '.o-summary_content' ).should( 'have.class', 'u-max-height-transition' );
      cy.get( '.o-summary_content' ).should( 'have.class', 'u-max-height-summary' );
      cy.get( '.o-summary_content' ).invoke( 'outerHeight' ).should( 'be.lte', 88 );
      answerPage.clickSummary();
      cy.get( '.o-summary_content' ).should( 'have.class', 'u-max-height-transition' );
      cy.get( '.o-summary_content' ).should( 'not.have.class', 'u-no-animation' );
      cy.get( '.o-summary_content' ).should( 'not.have.class', 'u-max-height-summary' );
      cy.get( '.o-summary_content' ).should( 'have.class', 'u-max-height-default' );
      cy.get( '.o-summary_content' ).invoke( 'outerHeight' ).should( 'be.gt', 88 );
    } );
  } );
} );
