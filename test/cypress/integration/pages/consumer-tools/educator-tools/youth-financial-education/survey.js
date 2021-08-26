const tests = [
  {
    name: 'should grade 3-5 survey with all first options',
    answers: [
      [0, 0, 0, 0, 0, 0],
      [0, 0],
      [0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0],
      [0, 0],
    ],
    resultsMatch: /^v1_3-5_10:z:h_/,
    x: [500, 500, 650, 300]
  },
  {
    name: 'should grade 3-5 survey with all last options',
    answers: [
      [3, 3, 3, 3, 3, 3],
      [3, 3],
      [3, 3, 3, 3, 3, 3, 3],
      [3, 3, 3],
      [3, 3],
    ],
    resultsMatch: /^v1_3-5_g:e:a_/,
    x: [40, 40, 40, 40]
  }
];

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

  // p5 => /done/
  // done sets cookie: resultUrl=...
  // done removes cookie: wizard_survey_wizard.
  // done => /results/

  cy.url().should( 'include', '/3-5/results/' );
  cy.getCookie( 'wizard_survey_wizard' ).should( 'not.exist' );
  cy.getCookie( 'resultUrl' )
    .then( cookie => {
      expect( cookie.value ).to.match( test.resultsMatch );
    } );
  cy.get( 'svg image' )
    .then( images => {
      test.x.forEach( ( val, idx ) => {
        expect( images[idx].getAttribute( 'x' ) ).to.equal( String( val ) );
      } );
    } );
}

describe( 'Youth Financial Education Survey', () => {
  describe( 'Completion', () => {
    beforeEach( () => {
    } );

    it( tests[0].name, () => testWithValues(tests[0]) );

    it( tests[1].name, () => testWithValues(tests[1]) );
  } );
} );
