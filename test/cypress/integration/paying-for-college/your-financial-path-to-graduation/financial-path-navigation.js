import { PfcFinancialPathToGraduation } from './your-financial-path-to-graduation-helpers';

const page = new PfcFinancialPathToGraduation();

describe( 'Paying For College navigation', () => {
  before( () => {
    cy.visit( '/paying-for-college/your-financial-path-to-graduation/' );
  } );
  it( 'should not navigate when program radios are not selected', () => {
    page.clickGetStarted( );
    page.enter( 'Harvard University' );
    page.searchResults().should( 'be.visible' );
    page.clickSearchResult( 'Harvard University' );
    page.clickNextStep( );
    cy.get( '#college-costs_school-search' ).should( 'be.visible' );
    page.clickLeftNav( 'costs' );
    cy.get( '#college-costs_school-search' ).should( 'be.visible' );
  } );

  it( 'should navigate the sections properly using the left-side nav', () => {
    page.selectProgram( 'type', 'bachelors' );
    page.selectProgram( 'years-spent', 'n' );
    page.selectProgram( 'length', '3' );
    page.selectProgram( 'housing', 'on-campus' );
    page.selectProgram( 'dependency', 'dependent' );
    page.clickLeftNav( 'costs' );
    cy.get( '[data-tool-section="costs"]' ).should( 'be.visible' );
    page.clickLeftNav( 'grants-scholarships' );
    cy.get( '[data-tool-section="grants-scholarships"]' ).should( 'be.visible' );
    page.clickLeftNav( 'work-study' );
    cy.get( '[data-tool-section="work-study"]' ).should( 'be.visible' );
  } );

  it( 'should show and hide the submenus of the secondary nav properly', () => {
    page.clickLeftNav( 'costs' );
    cy.get( '[data-nav_item="loan-counseling"]' ).should( 'not.be.visible' );
    cy.get( '[data-nav_section="covering-costs"]' ).click();
    cy.get( '[data-nav_item="loan-counseling"]' ).should( 'be.visible' );
  } );

  it( 'should not display costs inputs until a cost choice is made', () => {
    cy.get( '#costs-offer-button' ).click();
    cy.get( '#costs_inputs-section' ).should( 'not.be.visible' );
    page.costsQuestionChoice( 'yes' );
    cy.get( '#costs_inputs-section' ).should( 'be.visible' );
  } );

  it( 'should properly change pages when Next button is clicked', () => {
    page.clickNextStep();
    cy.get( '[data-tool-section="grants-scholarships"]' ).should( 'be.visible' );
  } );
} );
