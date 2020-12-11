import { PayingForCollege } from '../../components/paying-for-college/';

const page = new PayingForCollege();

describe( 'Paying for College', () => {
  beforeEach( () => {
    page.openLoan();
  } );
  describe( 'Choose a student loan', () => {
    it( 'should display answers to each question', () => {
      cy.get( '#_o1' ).click();
      cy.get( '#_o1' ).should( 'contain', 'I have to borrow money for school. What are my options?' );
      cy.get( '#answer1' ).should( 'be.visible' )
        .and( 'contain', 'If you have to take out student loans' );

      cy.get( '#_o2' ).click()
      cy.get( '#_o2' ).should( 'contain', "What if my grants and federal loans don't cover the cost of attendance?" );
      cy.get( '#answer2' ).should( 'be.visible' )
        .and( 'contain', 'If your grants and federal loans are not enough to cover the cost of your education' );

      cy.get( '#_o3' ).click()
      cy.get( '#_o3' ).should( 'contain', 'What should I consider when shopping for a private loan?' );
      cy.get( '#answer3' ).should( 'be.visible' )
        .and( 'contain', 'First, make sure you need a private student loan' );
    } );
    it( 'should display expandable comparison tables', () => {
      page.clickExpandable( 'Detailed comparison of Federal and Private loans' );
      cy.get( '.compare-table' ).should( 'be.visible' );
      page.clickExpandable( 'Detailed comparison of Federal and Private loans' );
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
      page.clickBubble( "What's the difference between subsidized and unsubsidized student loans?" );
      cy.get( '.bubble-transparent-answer' ).should( 'be.visible' )
        .and( 'contain', 'The government pays the interest on subsidized loans' );
      page.closeFirstBubble();
      cy.get( '.bubble-transparent-answer' ).should( 'not.be.visible' );

      page.clickBubble( 'What happened to Stafford Loans?' );
      cy.get( '.bubble-transparent-answer' ).should( 'be.visible' )
        .and( 'contain', 'These are now called Federal Direct Loans' );

      page.clickBubble( 'How often do student loan rates change?' );
      cy.get( '.bubble-transparent-answer' ).should( 'be.visible' )
        .and( 'contain', 'Congress has the authority to change federal student loan rates' );

      page.clickBubble( 'Should I use a credit card to cover my education costs?' );
      cy.get( '.bubble-transparent-answer' ).should( 'be.visible' )
        .and( 'contain', "Don't replace student loan debt with credit card debt" );

      page.clickBubble( "What if I can't repay my private student loan?" );
      cy.get( '.bubble-transparent-answer' ).should( 'be.visible' )
        .and( 'contain', 'Contact the company that services your student loan immediately' );
      page.closeLastBubble();

      page.closeAllBubbles();
      cy.get( '.bubble-transparent-answer' ).should( 'not.be.visible' );
    } );
  } );
} );
