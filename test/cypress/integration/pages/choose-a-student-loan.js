import { PayingForCollege } from '../../components/paying-for-college/';

const page = new PayingForCollege();

describe( 'Paying for College', () => {
  describe( 'Choose a student loan', () => {
    it( 'should display answers to each student loan question', () => {
      page.openLoanOption( 'o1' );
      cy.get( 'div' ).should( 'contain', 'I have to borrow money for school. What are my options?' );
      cy.get( '#answer1' ).should( 'contain', 'If you have to take out student loans' );
      page.openLoanOption( 'o2' );
      cy.get( 'div' ).should( 'contain', "What if my grants and federal loans don't cover the cost of attendance?" );
      cy.get( '#answer2' ).should( 'contain', 'If your grants and federal loans are not enough to cover the cost of your education' );
      page.openLoanOption( 'o3' );
      cy.get( 'div' ).should( 'contain', 'What should I consider when shopping for a private loan?' );
      cy.get( '#answer3' ).should( 'contain', 'First, make sure you need a private student loan' );
    } );
    it( 'should display options for each student loan', () => {
      page.openLoanOption( 'o2' );
      page.clickOption( 'Detailed comparison of Federal and Private loans' );
      cy.get( '.compare-table' ).should( 'be.visible' );
      page.clickOption( 'Detailed comparison of Federal and Private loans' );
      cy.get( '.compare-table' ).should( 'not.be.visible' );
      page.clickOption( 'Federal Loan Options' );
      cy.get( '#FederalLoanOptions' ).should( 'be.visible' );
      page.clickOption( 'Private Loan Options' );
      cy.get( '#PrivateLoanOptions' ).should( 'be.visible' );
      cy.get( '#FederalLoanOptions' ).should( 'not.be.visible' );
      page.clickOption( 'Private Loan Options' );
      cy.get( '#PrivateLoanOptions' ).should( 'not.be.visible' );
    } );
    it( 'should display answers to each student loan option', () => {
      page.openLoanOption( 'o3' );
      page.selectOption( "What's the difference between subsidized and unsubsidized student loans?" );
      cy.get( '.bubble-transparent-answer' ).should( 'be.visible' )
        .and( 'contain', 'The government pays the interest on subsidized loans' );
      page.closeFirstOption();
      cy.get( '.bubble-transparent-answer' ).should( 'not.be.visible' );
      page.selectOption( 'What happened to Stafford Loans?' );
      cy.get( '.bubble-transparent-answer' ).should( 'be.visible' )
        .and( 'contain', 'These are now called Federal Direct Loans' );
      page.selectOption( 'How often do student loan rates change?' );
      cy.get( '.bubble-transparent-answer' ).should( 'be.visible' )
        .and( 'contain', 'Congress has the authority to change federal student loan rates' );
      page.selectOption( 'Should I use a credit card to cover my education costs?' );
      cy.get( '.bubble-transparent-answer' ).should( 'be.visible' )
        .and( 'contain', "Don't replace student loan debt with credit card debt" );
      page.selectOption( "What if I can't repay my private student loan?" );
      cy.get( '.bubble-transparent-answer' ).should( 'be.visible' )
        .and( 'contain', 'Contact the company that services your student loan immediately' );
      page.closeLastOption();
      page.closeAllOptions();
      cy.get( '.bubble-transparent-answer' ).should( 'not.be.visible' );
    } );
  } );
} );
