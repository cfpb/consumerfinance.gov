function testWithValues(test) {
  const firsts = [ 1, 7, 9, 16, 19 ];

  cy.visit( '/consumer-tools/educator-tools/youth-financial-education/survey/3-5/p1/' );

  const firstLegendSelector = '.tdp-form > li:first-child legend';
  const submitSelector = '.o-well + div .m-btn-group button[type="submit"]';

  for (let i = 0; i < 5; i++) {
    cy.get( firstLegendSelector ).should( 'include.text', `${ firsts[i] }.` );

    test.answers[i].forEach( ( val, idx ) => {
      cy.get( `.tdp-form > li:nth-child(${ idx + 1 }) .a-label` )
        .then( labels => {
          labels[val].click();
        } );
    } );

    cy.get( submitSelector ).click();
  }

  /**
   * The survey POSTs the answers the final time to the last page URL: p5/.
   * p5/ validates the answers and redirects to done/.
   * done/ sets the cookie resultsUrl, and removes cookie wizard_survey_wizard.
   * done/ then redirects to results/.
   */
  cy.url().should( 'include', '/3-5/results/' );
  cy.getCookie( 'wizard_survey_wizard' ).should( 'not.exist' );
  cy.getCookie( 'resultUrl' )
    .then( cookie => {
      expect( cookie.value ).to.match( test.resultsMatch );
    } );
  cy.get( 'svg image' )
    .then( images => {
      test.carImageX.forEach( ( val, idx ) => {
        expect( images[idx].getAttribute( 'x' ) ).to.equal( String( val ) );
      } );
    } );
}

describe( 'Youth Financial Education Survey', () => {
  describe( 'Completion', () => {

    it( 'should grade 3-5 survey with all first options', () => testWithValues( {
      answers: [
        [0, 0, 0, 0, 0, 0],
        [0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0],
        [0, 0]
      ],
      resultsMatch: /^v1_3-5_10:z:h_/,
      carImageX: [500, 500, 650, 300]
    } ) );

    it( 'should grade 3-5 survey with all last options', () => testWithValues( {
      answers: [
        [3, 3, 3, 3, 3, 3],
        [3, 3],
        [3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3],
        [3, 3]
      ],
      resultsMatch: /^v1_3-5_g:e:a_/,
      carImageX: [40, 40, 40, 40]
    } ) );

    it( 'should reject direct requests for results', () => {
      cy.clearCookies();

      // Can't use visit() locally because 500
      cy.request( {
        url: '/consumer-tools/educator-tools/youth-financial-education/survey/3-5/results/',
        followRedirect: false,
      } ).then( resp => {
        expect( resp.redirectedToUrl ).to.include( '/assess/survey/' );
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
