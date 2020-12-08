import { PayingForCollege } from '../../components/paying-for-college/';

const page = new PayingForCollege();

describe( 'Paying for College', () => {
  describe( 'Manage your college money', () => {
    it( 'should display answers to each college money question', () => {
      page.openMoneyOption( 'o1' );
      cy.get( '#_o1' ).should( 'contain', 'When should I get a bank account?' );
      cy.get( '#answer1' ).should( 'contain', 'Choose an account as soon as possible' );
      page.openMoneyOption( 'o2' );
      cy.get( '#_o2' ).should( 'contain', 'How do I avoid paying unexpected fees?' );
      cy.get( '#answer2' ).should( 'contain', 'very few accounts charge no fees at all' );
      page.openMoneyOption( 'o3' );
      cy.get( '#_o3' ).should( 'contain', 'Do I have to get an account with the bank at my school?' );
      cy.get( '#answer3' ).should( 'contain', 'Schools cannot require you to use their bank' );
    } );
    it( 'should display options for college money', () => {
      page.openMoneyOption( 'o2' );
      page.clickOption( 'View Banking Options' );
      cy.get( '.compare-table' ).should( 'be.visible' );
      page.clickOption( 'View Banking Options' );
      cy.get( '.compare-table' ).should( 'not.be.visible' );
      page.clickOption( 'View aid disbursement options' );
      cy.get( '.compare-table' ).should( 'be.visible' );
      page.clickOption( 'View aid disbursement options' );
      cy.get( '.compare-table' ).should( 'not.be.visible' );
    } );
    it( 'should display answers to each college money option', () => {
      page.openMoneyOption( 'o3' );
      page.selectOption( 'What is a financial aid disbursement?' );
      cy.get( '.bubble-transparent-answer' ).should( 'be.visible' )
        .and( 'contain', 'Your financial aid disbursement is the money left' );
      page.closeFirstOption();
      cy.get( '.bubble-transparent-answer' ).should( 'not.be.visible' );
      page.selectOption( 'What are overdraft fees and how can I avoid them?' );
      cy.get( '.bubble-transparent-answer' ).should( 'be.visible' )
        .and( 'contain', 'When you spend more money than you have in your account' );
      page.closeLastOption();
      cy.get( '.bubble-transparent-answer' ).should( 'not.be.visible' );
    } );
  } );
} );
