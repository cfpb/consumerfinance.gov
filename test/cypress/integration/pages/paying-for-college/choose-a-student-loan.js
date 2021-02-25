import { PayingForCollege } from '../../../components/paying-for-college.js';

const page = new PayingForCollege();

describe( 'Paying for College', () => {
  beforeEach( () => {
    page.openLoan();
  } );
  describe( 'Choose a student loan', () => {
    it( 'should display answers to each question', () => {
      cy.get( '#_o1' ).click();
      cy.get( '#_o1' ).should( 'be.visible' );
      cy.get( '#answer1' ).should( 'be.visible' );

      cy.get( '#_o2' ).click();
      cy.get( '#_o2' ).should( 'be.visible' );
      cy.get( '#answer2' ).should( 'be.visible' );

      cy.get( '#_o3' ).click();
      cy.get( '#_o3' ).should( 'be.visible' );
      cy.get( '#answer3' ).should( 'be.visible' );
    } );
    it( 'should display expandable comparison tables', () => {
      page.clickExpandable(
        'Detailed comparison of Federal and Private loans'
      );
      cy.get( '.compare-table' ).should( 'be.visible' );
      page.clickExpandable(
        'Detailed comparison of Federal and Private loans'
      );
      cy.get( '.compare-table' ).should( 'not.be.visible' );

      page.clickExpandable( 'Federal Loan Options' );
      cy.get( '#FederalLoanOptions' ).should( 'be.visible' );

      page.clickExpandable( 'Private Loan Options' );
      cy.get( '#PrivateLoanOptions' ).should( 'be.visible' );
      cy.get( '#FederalLoanOptions' ).should( 'not.be.visible' );

      page.clickExpandable( 'Private Loan Options' );
      cy.get( '#PrivateLoanOptions' ).should( 'not.be.visible' );
    } );
    it( 'should display answers to each question', () => {
      page.clickBubble(
        'What\'s the difference between ' +
        'subsidized and unsubsidized student loans?'
      );
      cy.get( '.bubble-transparent-answer' ).should( 'be.visible' );
      page.closeFirstBubble();
      cy.get( '.bubble-transparent-answer' ).should( 'not.be.visible' );

      page.clickBubble( 'What happened to Stafford Loans?' );
      cy.get( '.bubble-transparent-answer' ).should( 'be.visible' );

      page.clickBubble(
        'How often do student loan rates change?'
      );
      cy.get( '.bubble-transparent-answer' ).should( 'be.visible' );

      page.clickBubble(
        'Should I use a credit card to cover my education costs?'
      );
      cy.get( '.bubble-transparent-answer' ).should( 'be.visible' );

      page.clickBubble(
        "What if I can't repay my private student loan?"
      );
      cy.get( '.bubble-transparent-answer' ).should( 'be.visible' );
      page.closeLastBubble();

      page.closeAllBubbles();
      cy.get( '.bubble-transparent-answer' ).should( 'not.be.visible' );
    } );
  } );
} );
