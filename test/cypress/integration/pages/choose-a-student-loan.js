import { PfcChooseStudentLoan } from '../../pages/paying-for-college/choose-a-student-loan/';

const page = new PfcChooseStudentLoan();

describe( 'Paying for College', () => {
  describe( 'Choose a student loan', () => {
    it( 'should display you have to take out student loans', () => {
      page.openOption( 'o1' );
      page.expandOption( 'Detailed comparison of Federal and Private loans' );
      cy.get( '.compare-table' ).should( 'be.visible' );
      page.selectOption( "What's the difference between subsidized and unsubsidized student loans?" );
      cy.get( '.bubble-transparent-answer' ).should( 'be.visible' );
      page.closeFirstOption();
      cy.get( '.bubble-transparent-answer' ).should( 'not.be.visible' );
      page.closeOption( 'The government pays the interest on subsidized loans' );
      page.selectOption( 'What happened to Stafford Loans?' );
      page.closeOption( 'These are now called Federal Direct Loans' );
    } );
    it( 'should display your grants and federal loans are not enough', () => {
      page.openOption( 'o2' );
      page.expandOption( 'Federal Loan Options' );
      cy.get( '#FederalLoanOptions' ).should( 'be.visible' );
      page.selectOption( 'How often do student loan rates change?' );
      cy.get( '.bubble-transparent-answer' ).should( 'be.visible' );
      page.closeOption( 'Congress has the authority to change federal student loan rates' );
      page.selectOption( 'Should I use a credit card to cover my education costs?' );
      page.closeOption( "Don't replace student loan debt with credit card debt" );
    } );
    it( 'should display make sure you need a private student loan', () => {
      page.openOption( 'o3' );
      page.expandOption( 'Private Loan Options' );
      cy.get( '#PrivateLoanOptions' ).should( 'be.visible' );
      page.selectOption( "What if I can't repay my private student loan?" );
      cy.get( '.bubble-transparent-answer' ).should( 'be.visible' );
      page.closeOption( 'Contact the company that services your student loan immediately' );
      page.closeLastOption();
      cy.get( '.bubble-transparent-answer' ).should( 'not.be.visible' );
    } );
  } );
} );
