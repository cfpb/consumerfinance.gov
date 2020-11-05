import { PfcChooseStudentLoan } from '../../pages/paying-for-college/choose-a-student-loan/';

const page = new PfcChooseStudentLoan();

describe( 'Paying for College', () => {
  describe( 'Choose a student loan', () => {
    it( 'should display you have to take out student loans', () => {
      page.open();
      page.openOption( 'o1' );
      page.expandOption( 'Detailed comparison of Federal and Private loans' );
      page.selectOption( "What's the difference between subsidized and unsubsidized student loans?" );
      page.closeOption( 'The government pays the interest on subsidized loans' );
      page.selectOption( 'What happened to Stafford Loans?' );
      page.closeOption( 'These are now called Federal Direct Loans' );
      page.closeFirstOption();
    } );
    it( 'should display your grants and federal loans are not enough', () => {
      page.open();
      page.openOption( 'o2' );
      page.expandOption( 'Federal Loan Options' );
      page.selectOption( 'How often do student loan rates change?' );
      page.closeOption( 'Congress has the authority to change federal student loan rates' );
      page.selectOption( 'Should I use a credit card to cover my education costs?' );
      page.closeOption( "Don't replace student loan debt with credit card debt" );
    } );
    it( 'should display make sure you need a private student loan', () => {
      page.open();
      page.openOption( 'o3' );
      page.expandOption( 'Private Loan Options' );
      page.selectOption( "What if I can't repay my private student loan?" );
      page.closeOption( 'Contact the company that services your student loan immediately' );
      page.closeLastOption();
    } );
  } );
} );
