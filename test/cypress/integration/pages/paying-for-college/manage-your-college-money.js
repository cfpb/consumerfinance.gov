import { PayingForCollege } from '../../../components/paying-for-college.js';

const page = new PayingForCollege();

describe( 'Paying for College', () => {
  beforeEach( () => {
    page.openMoney();
  } );
  describe( 'Manage your college money', () => {
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
      cy.get( '.bubble-transparent-answer' ).should( 'be.visible' );

      page.closeFirstBubble();
      cy.get( '.bubble-transparent-answer' ).should( 'not.be.visible' );

      page.clickBubble( 'What are overdraft fees and how can I avoid them?' );
      cy.get( '.bubble-transparent-answer' ).should( 'be.visible' );

      page.closeLastBubble();
      cy.get( '.bubble-transparent-answer' ).should( 'not.be.visible' );
    } );
  } );
} );
