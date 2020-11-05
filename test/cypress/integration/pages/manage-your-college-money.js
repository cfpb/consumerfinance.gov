import { PfcManageCollegeMoney } from '../../pages/paying-for-college/manage-your-college-money/';

const page = new PfcManageCollegeMoney();

describe( 'Paying for College', () => {
  describe( 'Manage your college money', () => {
    it( 'should display Choose an account as soon as possible', () => {
      page.open();
      page.openOption( 'o1' );
      page.expandOption( 'View Banking Options' );
      page.selectOption( 'What is a financial aid disbursement?' );
      page.closeOption( 'Your financial aid disbursement is the money left' );
      page.closeFirstOption();
    } );
    it( 'should display very few accounts charge no fees at all', () => {
      page.open();
      page.openOption( 'o2' );
    } );
    it( 'should display Schools cannot require you to use their bank', () => {
      page.open();
      page.openOption( 'o3' );
      page.expandOption( 'View aid disbursement options' );
      page.selectOption( 'What are overdraft fees and how can I avoid them?' );
      page.closeOption( 'When you spend more money than you have in your account' );
      page.closeLastOption();
    } );
  } );
} );
