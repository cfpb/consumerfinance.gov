import { TdpResultsHelpers } from './results-helpers';
import { TdpSurveyHelpers } from './survey-helpers';

const results = new TdpResultsHelpers();
const survey = new TdpSurveyHelpers();

function testFillingSurvey( test ) {
  survey.open( `${ test.grades }/p1` );

  test.firstQ.forEach( ( val, idx ) => {
    survey.getFirstLegend().should( 'include.text', `${ val }.` );
    survey.selectAnswers( test.answers[idx] );
    survey.clickNext();
  } );
}

function testResultsPage( test ) {
  /**
   * The survey POSTs the answers the final time to the last page URL: p5/.
   * p5/ validates the answers and redirects to done/.
   * done/ sets the cookie resultsUrl, and removes cookie wizard_survey_wizard.
   * done/ then redirects to results/.
   */
  cy.url().should( 'include', results.getPath( test.grades ) );
  results.checkStudentCookies( test.resultsMatch );
  results.checkCarPositions( test.carImageX );
}

function testSharing( test ) {
  results.visitSharedUrl();
  results.checkInitials();
  results.checkCarPositions( test.carImageX );
  results.checkNoSharing();
}

describe( 'Youth Financial Education Survey', () => {
  describe( 'Starting over', () => {
    beforeEach( () => {
      cy.clearCookies();
      cy.window().then( win => win.sessionStorage.clear() );
    } );

    it( 'has the modal', () => {
      survey.open( '3-5/p1/' );
      survey.selectAnswers( [ 0, 0, 0, 0, 0, 0 ] );
      survey.clickNext();

      cy.get( '[data-open-modal="modal-restart"]' ).click();
      cy.get( '#modal-restart_desc' )
        .should( 'be.visible' )
        .should( 'include.text', 'Starting over will clear' );
    } );

    it( 'can return without changes', () => {
      survey.open( '3-5/p1/' );
      survey.selectAnswers( [ 0, 0, 0, 0, 0, 0 ] );
      survey.clickNext();
      cy.get( '[data-open-modal="modal-restart"]' ).click();

      // close via "Return"
      cy.get( '[data-cancel="1"]' ).click();
      cy.get( '#modal-restart_desc' ).should( 'be.hidden' );
      cy.getCookie( 'wizard_survey_wizard' ).then( cookie => {
        expect( cookie.value ).include( 'survey_wizard-current_step' );
      } );
      cy.window().then( win => {
        expect( win.sessionStorage.getItem( 'tdp-survey-choices' ) )
          .include( '"p1-q1":"0"' );
      } );

      // close button
      cy.get( '[data-open-modal="modal-restart"]' ).click();
      cy.get( '#modal-restart .o-modal_close' ).click();
      cy.get( '#modal-restart_desc' ).should( 'be.hidden' );
      cy.getCookie( 'wizard_survey_wizard' ).then( cookie => {
        expect( cookie.value ).include( 'survey_wizard-current_step' );
      } );
      cy.window().then( win => {
        expect( win.sessionStorage.getItem( 'tdp-survey-choices' ) )
          .include( '"p1-q1":"0"' );
      } );
    } );

    it( 'can reset', () => {
      survey.open( '3-5/p1/' );
      survey.selectAnswers( [ 0, 0, 0, 0, 0, 0 ] );
      survey.clickNext();
      cy.get( '[data-open-modal="modal-restart"]' ).click();

      cy.intercept('**/p1/', req => {
        req.url = survey.url( '3-5/p1/' );
      });
      cy.get( '[data-cancel=""]' ).click();
    } );
  } );

  describe( 'Completion', () => {
    beforeEach( () => {
      Cypress.Cookies.preserveOnce('wizard_survey_wizard', 'resultUrl');
    } );

    const tests = [
      {
        name: 'Grade 3-5 choosing first',
        grades: '3-5',
        firstQ: [ 1, 7, 9, 16, 19 ],
        answers: [
          [ 0, 0, 0, 0, 0, 0 ],
          [ 0, 0 ],
          [ 0, 0, 0, 0, 0, 0, 0 ],
          [ 0, 0, 0 ],
          [ 0, 0 ]
        ],
        resultsMatch: /^v1_3-5_10:z:h_/,
        carImageX: [ 500, 500, 650, 300 ]
      },
      {
        name: 'Grade 3-5 choosing last',
        grades: '3-5',
        firstQ: [ 1, 7, 9, 16, 19 ],
        answers: [
          [ 3, 3, 3, 3, 3, 3 ],
          [ 3, 3 ],
          [ 3, 3, 3, 3, 3, 3, 3 ],
          [ 3, 3, 3 ],
          [ 3, 3 ]
        ],
        resultsMatch: /^v1_3-5_g:e:a_/,
        carImageX: [ 40, 40, 40, 40 ]
      }
    ];

    for (const test of tests) {
      // Order matters here
      it( `can fill survey ${ test.name }`, () => testFillingSurvey( test ) );
      it( `can score survey ${ test.name }`, () => testResultsPage( test ) );
      it( `can print survey ${ test.name }`, () => results.print() );
      it( `can share survey ${ test.name }`, () => testSharing( test ) );
    }
  } );

  describe( 'Redirects', () => {
    it( 'should reject direct requests for results', () => {
      cy.clearCookies();

      cy.url().then( url => {
        /**
         * The wagtail page that gets redirected to is only available on the
         * prod and beta environments, so the tests differ.
         */
        const prodBetaPattern = /\/\/(beta|www)\.consumerfinance\.gov\b/;
        const wagtailPageExists = prodBetaPattern.test( url );
        if ( wagtailPageExists ) {
          cy.visit( '/consumer-tools/educator-tools/youth-financial-education/survey/3-5/results/' );
          cy.get( '#choose-your-grade-level-to-begin h2' ).should( 'exist' );
        } else {
          // Must capture where we get redirected to.
          cy.request( {
            url: '/consumer-tools/educator-tools/youth-financial-education/survey/3-5/results/',
            followRedirect: false
          } ).then( resp => {
            expect( resp.redirectedToUrl ).to.include( '/assess/survey/' );
          } );
        }
      } );
    } );

    it( 'should reject jumping later into survey', () => {
      cy.window().then( win => {
        win.sessionStorage.clear();
      } );

      cy.visit( '/consumer-tools/educator-tools/youth-financial-education/survey/3-5/p2/' );
      cy.url().should( 'include', '/3-5/p1/' );
    } );
  } );
} );
