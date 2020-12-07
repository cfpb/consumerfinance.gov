import { PfcManageCollegeMoney } from '../../pages/paying-for-college/manage-your-college-money/';

const page = new PfcManageCollegeMoney();

describe( 'Paying for College', () => {
  describe( 'Manage your college money', () => {
    it( 'should display Choose an account as soon as possible', () => {
      page.openOption( 'o1' );
      cy.get( '#answer1' ).contains( 'Choose an account as soon as possible' );
      page.expandOption( 'View Banking Options' );
      cy.get( '.compare-table' ).should( 'be.visible' );
      page.selectOption( 'What is a financial aid disbursement?' );
      cy.get( '.bubble-transparent-answer' ).should( 'be.visible' );
      page.closeOption( 'Your financial aid disbursement is the money left' );
      page.closeFirstOption();
      cy.get( '.bubble-transparent-answer' ).should( 'not.be.visible' );
    } );
    it( 'should display very few accounts charge no fees at all', () => {
      page.openOption( 'o2' );
      cy.get( '#answer2' ).contains( 'very few accounts charge no fees at all' );
    } );
    it( 'should display Schools cannot require you to use their bank', () => {
      page.openOption( 'o3' );
      cy.get( '#answer3' ).contains( 'Schools cannot require you to use their bank' );
      page.expandOption( 'View aid disbursement options' );
      cy.get( '.compare-table' ).should( 'be.visible' );
      page.selectOption( 'What are overdraft fees and how can I avoid them?' );
      cy.get( '.bubble-transparent-answer' ).should( 'be.visible' );
      page.closeOption( 'When you spend more money than you have in your account' );
      page.closeLastOption();
      cy.get( '.bubble-transparent-answer' ).should( 'not.be.visible' );
    } );
  } );
} );
