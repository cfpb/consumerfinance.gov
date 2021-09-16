export class TdpSurveyPage {
  open( path ) {
    path = path.replace( /(^\/|\/$)/, '' ) + '/';
    cy.visit( `/consumer-tools/educator-tools/youth-financial-education/survey/${ path }` );
  }

  selectAnswers( answers ) {
    answers.forEach( ( val, idx ) => {
      cy.get( `.tdp-form > li:nth-child(${ idx + 1 }) .a-label` )
        .then( labels => {
          labels[val].click();
        } );
    } );
  }

  getFirstLegend() {
    return cy.get( '.tdp-form > li:first-child legend' );
  }

  clickNext() {
    cy.get( '.o-well + div .m-btn-group button[type="submit"]' ).click();
  }
}
