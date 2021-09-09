import { TdpSurveyHelpers } from './survey-helpers';

const survey = new TdpSurveyHelpers();

describe( 'Youth Financial Education Survey: Progress', () => {
  function verifyProgress( numDone, percent ) {
    cy.get( '.tdp-survey-progress-out-of' ).should( 'include.text', `${ numDone } of`);
    cy.get( '.tdp-survey-progress__svg text:nth-of-type(1)')
      .should( 'include.text', `${ percent }%` );
    cy.get( '.tdp-survey-progress__svg text:nth-of-type(1)')
      .should( 'include.text', `${ percent }%` );
  }

  it( 'tracks page progress', () => {
    cy.window().then( win => win.sessionStorage.clear() );
    survey.open( '3-5/p1' );
    verifyProgress( 0, 0 );

    survey.selectAnswers( [ 0, 0, 0 ] );
    verifyProgress( 3, 15 );
    cy.get( '.tdp-survey-section:first-child .tdp-survey-section__icon svg')
      .should( 'be.hidden' );

    survey.selectAnswers( [ null, null, null, 0, 0, 0 ] );
    verifyProgress( 6, 30 );
    cy.get( '.tdp-survey-section:first-child .tdp-survey-section__icon svg')
      .should( 'be.visible' );

    survey.clickNext();
    verifyProgress( 6, 30 );

    survey.selectAnswers( [ 0, 0 ] );
    verifyProgress( 8, 40 );
  } );

  function verifySectionColors( colors ) {
    cy.get( '.tdp-survey-section' ).then( $buttons => {
      let canBeEdited = true;

      $buttons.each( ( idx, button ) => {
        expect( button.getAttribute( 'data-color' ) )
          .equal( colors[idx] ? colors[idx] : 'gray' );
        if (colors[idx] === 'blue') {
          canBeEdited = false;
        }

        expect( button.getAttribute( 'data-editable' ) )
          .equal( ( colors[idx] === 'green' && canBeEdited ) ? '1' : '' );
      } );
    } );
  }

  it( 'updates section UI', () => {
    cy.window().then( win => win.sessionStorage.clear() );
    survey.open( '3-5/p1' );
    verifySectionColors( [ 'blue' ] );
    survey.selectAnswers( [ 0, 0, 0, 0, 0, 0 ] );
    survey.clickNext();

    verifySectionColors( [ 'green', 'blue' ] );
    survey.selectAnswers( [ 0, 0 ] );
    survey.clickNext();

    verifySectionColors( [ 'green', 'green', 'blue' ] );
    cy.get( '.tdp-survey-section:first-child .tdp-survey-section__edit span')
      .click();

    verifySectionColors( [ 'blue', 'green', 'white' ] );
    survey.clickNext();

    verifySectionColors( [ 'green', 'blue', 'white' ] );
    survey.clickNext();

    verifySectionColors( [ 'green', 'green', 'blue' ] );
  } );

  it( 'stores answers without submit', () => {
    cy.window().then( win => win.sessionStorage.clear() );
    survey.open( '3-5/p1' );
    survey.selectAnswers( [ 0, 0, 0 ] );

    survey.open( '3-5/p1' );
    verifyProgress( 3, 15 );

    survey.selectAnswers( [ 0, 0, 0, 0, 0, 0 ] );
    survey.clickNext();

    survey.selectAnswers( [ 0 ] );
    cy.get( 'a[href="../p1/"]' ).click();

    cy.url().should( 'include', '/p1/' );
    survey.clickNext();

    cy.get( '#id_p2-q7_0' ).should( 'be.checked' );
  } );
} );
