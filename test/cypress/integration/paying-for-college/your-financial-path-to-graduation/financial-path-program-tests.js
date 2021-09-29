import { PfcFinancialPathToGraduation } from './your-financial-path-to-graduation-helpers';

const page = new PfcFinancialPathToGraduation();

describe( 'Paying For College program-based content', () => {
  before( () => {
    cy.intercept( '/paying-for-college2/understanding-your-financial-aid-offer/api/constants/', { fixture: 'constants' } ).as( 'constants' );
    cy.visit( '/paying-for-college/your-financial-path-to-graduation/' );
  } );

  it( 'should enforce Direct federal loan limits based on the constants API values', () => {
    page.clickGetStarted( );
    page.enter( 'Harvard University' );
    page.searchResults().should( 'be.visible' );
    page.clickSearchResult( 'Harvard University' );
    page.selectProgram( 'type', 'certificate' );
    page.selectProgram( 'years-spent', 'n' );
    page.selectProgram( 'length', '1' );
    page.selectProgram( 'housing', 'on-campus' );
    page.selectProgram( 'dependency', 'dependent' );
    page.clickLeftNav( 'federal-loans' );
    page.setText( 'loans__directSub', '999999' );
    cy.get( '#loans__directSub' ).blur();
    cy.get( '#loans__directSub' ).should( 'have.value', '$1,000' );
    page.setText( 'loans__directUnsub', '999999' );
    cy.get( '#loans__directUnsub' ).blur();
    cy.get( '#loans__directUnsub' ).should( 'have.value', '$4,500' );
  } );

  it( 'should change limits when the user changes their program progress', () => {
    page.clickLeftNav( 'school-info' );
    page.selectProgram( 'years-spent', '1' );
    page.clickLeftNav( 'federal-loans' );
    page.setText( 'loans__directSub', '999999' );
    cy.get( '#loans__directSub' ).blur();
    cy.get( '#loans__directSub' ).should( 'have.value', '$2,000' );
    page.setText( 'loans__directUnsub', '999999' );
    cy.get( '#loans__directUnsub' ).blur();
    cy.get( '#loans__directUnsub' ).should( 'have.value', '$5,500' );

    page.clickLeftNav( 'school-info' );
    page.selectProgram( 'years-spent', 'a' );
    page.clickLeftNav( 'federal-loans' );
    page.setText( 'loans__directSub', '999999' );
    cy.get( '#loans__directSub' ).blur();
    cy.get( '#loans__directSub' ).should( 'have.value', '$3,000' );
    page.setText( 'loans__directUnsub', '999999' );
    cy.get( '#loans__directUnsub' ).blur();
    cy.get( '#loans__directUnsub' ).should( 'have.value', '$6,500' );
  } );

  it( 'should display associates content for associates students', () => {
    cy.get( '[data-nav_section="worth-investment"]' ).click();
    page.clickLeftNav( 'action-plan' );
    page.actionPlan( 'put-into-action' );
    cy.get( '[data-state-based-visibility="put-into-action"] .associates-content' ).should( 'be.visible' );
    cy.get( '[data-state-based-visibility="put-into-action"] .graduate-content' ).should( 'not.be.visible' );
  } );


  it( 'should display undergrad content for undergrad students', () => {
    cy.get( '[data-nav_section="worth-investment"]' ).click();
    page.clickLeftNav( 'action-plan' );
    page.actionPlan( 'put-into-action' );
    cy.get( '[data-state-based-visibility="put-into-action"] .undergrad-content' ).should( 'be.visible' );
    cy.get( '[data-state-based-visibility="put-into-action"] .graduate-content' ).should( 'not.be.visible' );

    cy.get( '[data-nav_section="offer-letter"]' ).click();
    page.clickLeftNav( 'school-info' );
    page.selectProgram( 'type', 'bachelors' );
    cy.get( '[data-nav_section="worth-investment"]' ).click();
    page.clickLeftNav( 'action-plan' );
    page.actionPlan( 'put-into-action' );
    cy.get( '[data-state-based-visibility="put-into-action"] .undergrad-content' ).should( 'be.visible' );
    cy.get( '[data-state-based-visibility="put-into-action"] .graduate-content' ).should( 'not.be.visible' );

    cy.get( '[data-nav_section="offer-letter"]' ).click();
    page.clickLeftNav( 'school-info' );
    page.selectProgram( 'type', 'certificate' );
    cy.get( '[data-nav_section="worth-investment"]' ).click();
    page.clickLeftNav( 'action-plan' );
    page.actionPlan( 'put-into-action' );
    cy.get( '[data-state-based-visibility="put-into-action"] .undergrad-content' ).should( 'be.visible' );
    cy.get( '[data-state-based-visibility="put-into-action"] .graduate-content' ).should( 'not.be.visible' );
  } );

  it( 'should display graduate content for graduate students', () => {
    cy.get( '[data-nav_section="offer-letter"]' ).click();
    page.clickLeftNav( 'school-info' );
    page.selectProgram( 'type', 'graduate' );
    cy.get( '[data-nav_section="worth-investment"]' ).click();
    page.clickLeftNav( 'action-plan' );
    page.actionPlan( 'put-into-action' );
    cy.get( '[data-state-based-visibility="put-into-action"] .graduate-content' ).should( 'be.visible' );
    cy.get( '[data-state-based-visibility="put-into-action"] .undergrad-content' ).should( 'not.be.visible' );
  } );
} );
