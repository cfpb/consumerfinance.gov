import { closest } from '../../../js/modules/util/dom-traverse';
import { hide, show, slide } from './repay-utils';
import { elemContainsElem } from './quiz-utils';

const quizHandler = function( container ) {
  const handler = {};
  handler.container = container;
  handler.questions = container.querySelectorAll( '.quiz__question' );
  handler.responses = container.querySelectorAll( '.quiz__answer-response' );

  const handleButtons = () => {
    handler.questions.forEach( question => {
      const buttons = question.querySelectorAll( '.quiz__response-button' );
      buttons.forEach( button => {
        button.addEventListener( 'click', event => {
          event.preventDefault();
          const answerSection = closest( event.target, '.quiz__answers' );
          const responseTarget = answerSection.querySelector( '.quiz__response-target' );
          const checked = answerSection.querySelector( 'input:checked' );
          const checkedAnswer = closest( checked, '.quiz__answer' );
          const checkedResponse = checkedAnswer.querySelector( '.quiz__answer-response' );
          const clone = checkedResponse.cloneNode( true );

          // clear target area & append clone
          let first = responseTarget.firstElementChild;
          while ( first ) {
            responseTarget.removeChild( first );
            first = responseTarget.firstElementChild;
          }
          responseTarget.appendChild( clone );

          slide( 'down', clone );

        } );


        /* const input = buttonArea.querySelector( '.a-label' );
           input.addEventListener( 'click', ( event ) => {
           // TODO - Refactor this once we have IDs working
           const answer = closest( event.target, '.quiz__answer' );
           const answerSection = closest( event.target, '.quiz__answers' );
           const radioButtons = answerSection.querySelectorAll( 'input[type="radio"]' );
           radioButtons.forEach( ( button ) => {
           button.checked = false;
           } ); */

        /* const radioResponses = answerSection.querySelectorAll( '.quiz__answer-response' );
           radioResponses.forEach( ( elem ) => { */

        /* if ( !elemContainsElem( answer, elem ) ) {
           hide( elem );
           // slide( 'up', elem );
           }
           } ); */

        /* const clickedButton = closest( event.target, '.quiz__answer')
           .querySelector( 'input[type="radio"]' );
           clickedButton.checked = true; */

        /* const response = answer.querySelector( '.quiz__answer-response' );
           if ( response !== null ) {
           // show( response );
           slide( 'down', response );
           } */

        // } );
      } );
    } );
  };

  const init = () => {
    // hide responses
    handler.responses.forEach( response => {
      hide( response );
    } );

    // TODO - Remove this when we get IDs working
    const qsecs = document.querySelectorAll( '.quiz__answer-choice' );
    qsecs.forEach( ( div, i ) => {
      div.querySelector( 'input' ).setAttribute( 'id', 'answerChoice' + i );
      div.querySelector( 'label' ).setAttribute( 'for', 'answerChoice' + i );
    } );

    handleButtons();
  };


  init();

  return handler;
};

const init = function() {
  console.log( 'Initializing...' );

  const quizContainers = document.querySelectorAll( '.quiz__container' );
  quizContainers.forEach( container => {
    const quiz = quizHandler( container );
  } );

  console.log( 'Initialized!' );
};


if ( 'replaceState' in window.history ) {
  window.addEventListener( 'load', init );
}
