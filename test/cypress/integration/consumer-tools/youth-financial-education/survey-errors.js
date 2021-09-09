import { TdpSurveyHelpers } from './survey-helpers';

const survey = new TdpSurveyHelpers();

describe( 'Youth Financial Education Survey: Errors', () => {
  function refreshErrors() {
    cy.window().then( win => win.sessionStorage.clear() );
    survey.open( '3-5/p1' );
    survey.selectAnswers( [0, 0, null, 0, 0, null] );
    survey.clickNext();
  }

  it( 'alerts of missing questions', () => {
    refreshErrors();
    cy.wait( 700 );
    cy.window().then( win => {
      expect( win.scrollY ).lessThan( 287 );
    } );
    cy.get( 'form .m-notification__error ' )
      .should( 'be.visible' )
      .should( 'include.text', 'You\'ve missed a question.' );
    cy.get( 'form .m-notification__error a' ).should( 'have.length', 2);

    cy.get( 'form .m-notification__error li:nth-child(1) a' )
      .should( 'include.text', '3.' );
    cy.get( '.tdp-form > li:nth-child(3) .a-form-alert_text' )
      .should( 'include.text', 'You forgot');

    cy.get( 'form .m-notification__error li:nth-child(2) a' )
      .should( 'include.text', '6.' );
    cy.get( '.tdp-form > li:nth-child(6) .a-form-alert_text' )
      .should( 'include.text', 'You forgot');
  } );

  it( 'links jump to questions', () => {
    refreshErrors();
    cy.get( 'form .m-notification__error li:nth-child(2) a' )
      .click();
    cy.wait( 700 );
    cy.window().then( win => {
      expect( win.scrollY ).greaterThan( 1200 );
    } );
  } );

  it( 'warns until none missing', () => {
    refreshErrors();
    survey.selectAnswers( [null, null, null, null, null, 0] );
    survey.clickNext();
    cy.get( 'form .m-notification__error ' ).should( 'be.visible' );
    cy.get( 'form .m-notification__error a' )
      .should( 'have.length', 1)
      .should( 'include.text', '3.' );
    cy.get( '.tdp-form > li:nth-child(6) .a-form-alert_text' )
      .should( 'not.exist' );

    survey.selectAnswers( [null, null, 0] );
    survey.clickNext();
    cy.url().should( 'include', '/3-5/p2/' );
  } );
} );
