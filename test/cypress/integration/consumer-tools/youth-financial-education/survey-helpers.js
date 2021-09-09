export class TdpSurveyHelpers {
  open( path ) {
    cy.visit( this.url( path) );
  }

  url( path ) {
    path = path.replace( /(^\/|\/$)/, '' ) + '/';
    return `/consumer-tools/educator-tools/youth-financial-education/survey/${ path }`;
  }

  selectAnswers( answers ) {
    answers.forEach( ( val, idx ) => {
      if ( val !== null ) {
        cy.get( `.tdp-form > li:nth-child(${ idx + 1 }) .a-label` )
          .then( labels => {
            labels[val].click();
          } );
      }
    } );
  }

  getFirstLegend() {
    return cy.get( '.tdp-form > li:first-child legend' );
  }

  clickNext() {
    cy.get( '.o-well + div .m-btn-group button[type="submit"]' ).click();
  }
}
