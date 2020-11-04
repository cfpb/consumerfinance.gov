import { PfcRepayStudentDebt } from '../../pages/paying-for-college/repay-student-debt/';

const page = new PfcRepayStudentDebt();

describe( 'Paying for College', () => {
  describe( 'Repay student debt', () => {
    it( 'should display Direct debit and extra payments', () => {
      page.open();
      page.click( 'Federal' );
      page.selectQuestion ( '2' );
      page.click( 'Yes' );
      page.selectQuestion ( '3' );
      page.click( 'Not sure' );
      page.selectQuestion ( '4' );
      page.click( 'Yes' );
      page.selectQuestion ( '5' );
      page.click( 'No' );
    } );
    it( 'should display Lower your interest rate', () => {
      page.open();
      page.click( 'Non-Federal' );
      page.selectQuestion ( '2' );
      page.click( 'Yes' );
      page.selectQuestion ( '3' );
      page.click( 'Not sure' );
      page.selectQuestion ( '4' );
      page.click( 'No' );
      page.selectQuestion ( '5' );
      page.click( 'Yes' );
    } );
    it( 'should display Payment plans based on your income', () => {
      page.open();
      page.click( 'Federal' );
      page.click( 'Yes' );
      page.click( 'Yes' );
      page.click( 'Yes' );
    } );
    it( 'should display Reach out to your loan servicer', () => {
      page.open();
      page.click( 'Federal' );
      page.click( 'No' );
      page.click( 'No' );
      page.click( 'No' );
    } );
    it( 'should display Federal direct consolidation loans', () => {
      page.open();
      page.click( 'Federal' );
      page.click( 'Yes' );
      page.click( 'No' );
      page.click( 'Yes' );
    } );
    it( 'should display Getting ahead on your private student loan', () => {
      page.open();
      page.click( 'Non-Federal' );
      page.click( 'No' );
      page.click( 'Yes' );
      page.click( 'No' );
    } );
    it( 'should display Getting out of default when you face debt collection', () => {
      page.open();
      page.click( 'Non-Federal' );
      page.click( 'Yes' );
      page.click( 'Yes' );
    } );
  } );
} );
