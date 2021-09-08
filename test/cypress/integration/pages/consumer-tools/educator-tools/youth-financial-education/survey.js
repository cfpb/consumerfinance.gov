import { TdpResultsPage } from '../../../../../pages/consumer-tools/educator-tools/youth-financial-education/results';
import { TdpSurveyPage } from '../../../../../pages/consumer-tools/educator-tools/youth-financial-education/survey';

const results = new TdpResultsPage();
const survey = new TdpSurveyPage();

function testWithValues( test ) {
  survey.open( `${ test.grades }/p1` );

  test.firstQ.forEach( ( val, idx ) => {
    survey.getFirstLegend().should( 'include.text', `${ val }.` );
    survey.selectAnswers( test.answers[idx] );
    survey.clickNext();
  } );

  /**
   * The survey POSTs the answers the final time to the last page URL: p5/.
   * p5/ validates the answers and redirects to done/.
   * done/ sets the cookie resultsUrl, and removes cookie wizard_survey_wizard.
   * done/ then redirects to results/.
   */
  cy.url().should( 'include', results.getPath( test.grades ) );
  results.checkStudentCookies( test.resultsMatch );
  results.checkCarPositions( test.carImageX );

  results.visitSharedUrl();
  results.checkInitials();
  results.checkCarPositions( test.carImageX );
  results.checkNoSharing();
}

describe( 'Youth Financial Education Survey', () => {
  describe( 'Completion', () => {
    it( 'should grade 3-5 survey with all first options', () => testWithValues( {
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
    } ) );

    it( 'should grade 3-5 survey with all last options', () => testWithValues( {
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
    } ) );
  } );

  describe( 'Redirects', () => {
    it( 'should reject direct requests for results', () => {
      cy.clearCookies();

      cy.url().then( url => {
        /**
         * The wagtail page that gets redirected to is only available on the
         * prod and beta environments, so the tests differ.
         */
        const prodBetaPattern = /\/\/(beta|www).consumerfinance.gov\b/;
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
