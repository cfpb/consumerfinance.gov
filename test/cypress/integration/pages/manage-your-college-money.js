import { PayingForCollege } from '../../components/paying-for-college/';

const page = new PayingForCollege();

describe( 'Paying for College', () => {
  beforeEach( () => {
    page.openMoney();
  } );
  describe( 'Manage your college money', () => {
    it( 'should display answers to each question', () => {
      cy.get( '#_o1' ).click();
      cy.get( '#_o1' ).should( 'be.visible' )
        .and( 'contain', 'When should I get a bank account?' );
      cy.get( '#answer1' ).should( 'be.visible' )
        .and( 'contain', 'Choose an account as soon as possible' );

      cy.get( '#_o2' ).click();
      cy.get( '#_o2' ).should( 'be.visible' )
        .and( 'contain', 'How do I avoid paying unexpected fees?' );
      cy.get( '#answer2' ).should( 'be.visible' )
        .and( 'contain', 'very few accounts charge no fees at all' );

      cy.get( '#_o3' ).click();
      cy.get( '#_o3' ).should( 'be.visible' )
        .and( 'contain', 'Do I have to get an account with the bank at my school?' );
      cy.get( '#answer3' ).should( 'be.visible' )
        .and( 'contain', 'Schools cannot require you to use their bank' );
    } );
    it( 'should display expandable comparison tables', () => {
      page.clickExpandable( 'View Banking Options' );
      cy.get( '.compare-table' ).should( 'be.visible' );

      page.clickExpandable( 'View Banking Options' );
      cy.get( '.compare-table' ).should( 'not.be.visible' );

      page.clickExpandable( 'View aid disbursement options' );
      cy.get( '.compare-table' ).should( 'be.visible' );

      page.clickExpandable( 'View aid disbursement options' );
      cy.get( '.compare-table' ).should( 'not.be.visible' );
    } );
    it( 'should display answers to each question', () => {
      page.clickBubble( 'What is a financial aid disbursement?' );
      cy.get( '.bubble-transparent-answer' ).should( 'be.visible' )
        .and( 'contain', 'Your financial aid disbursement is the money left' );

      page.closeFirstBubble();
      cy.get( '.bubble-transparent-answer' ).should( 'not.be.visible' );

      page.clickBubble( 'What are overdraft fees and how can I avoid them?' );
      cy.get( '.bubble-transparent-answer' ).should( 'be.visible' )
        .and( 'contain', 'When you spend more money than you have in your account' );

      page.closeLastBubble();
      cy.get( '.bubble-transparent-answer' ).should( 'not.be.visible' );
    } );
  } );
} );
