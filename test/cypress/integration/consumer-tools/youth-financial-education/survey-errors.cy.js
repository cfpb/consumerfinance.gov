import { TdpSurveyHelpers } from './survey-helpers.cy.js';

const survey = new TdpSurveyHelpers();

/**
 * Reset test state.
 */
function refreshErrors() {
  cy.window().then((win) => win.sessionStorage.clear());
  survey.open('3-5/p1');
  survey.selectAnswers([0, 0, null, 0, 0, null]);
  survey.clickNext();
}

describe('Youth Financial Education Survey: Errors', () => {
  /**
   * TODO: This scroll test frequently fails on headless runs in our pipeline.
   * We'll skip it for now, but we should come back to it in a future version
   * of Cypress to see if it's working reliably.
   *
   * See https://github.com/cfpb/consumerfinance.gov/pull/7450 for a possibly
   * related issue with smooth scrolling in Cypress tests.
   */
  xit('jumps to errors at top', () => {
    refreshErrors();
    cy.get('.m-notification__visible');
    cy.get('main h1').isScrolledTo();
  });

  it('alerts of missing questions', () => {
    refreshErrors();
    cy.get('form .m-notification__error ')
      .should('be.visible')
      .should('include.text', "You've missed a question.");
    cy.get('form .m-notification__error a').should('have.length', 2);

    cy.get('form .m-notification__error li:nth-child(1) a').should(
      'include.text',
      '3.'
    );
    cy.get('.tdp-form > li:nth-child(3) .a-form-alert_text').should(
      'include.text',
      'You forgot'
    );

    cy.get('form .m-notification__error li:nth-child(2) a').should(
      'include.text',
      '6.'
    );
    cy.get('.tdp-form > li:nth-child(6) .a-form-alert_text').should(
      'include.text',
      'You forgot'
    );
  });

  xit('links jump to questions', () => {
    refreshErrors();
    cy.get('form .m-notification__error li:nth-child(2) a').click();
    cy.get('.survey-reset--link--wrap').isScrolledTo();
  });

  it('warns until none missing', () => {
    refreshErrors();
    survey.selectAnswers([null, null, null, null, null, 0]);
    survey.clickNext();
    cy.get('form .m-notification__error ').should('be.visible');
    cy.get('form .m-notification__error a')
      .should('have.length', 1)
      .should('include.text', '3.');
    cy.get('.tdp-form > li:nth-child(6) .a-form-alert_text').should(
      'not.exist'
    );

    survey.selectAnswers([null, null, 0]);
    survey.clickNext();
    cy.url().should('include', '/3-5/p2/');
  });
});
