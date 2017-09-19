/* eslint no-global-assign: "off" */
'use strict';

var Analytics = require( '../../modules/Analytics' );

( function() {

  var totalQuestions = 12;
  var quizComplete = false;
  var questionValues = {};

  var submitInput = document.querySelector( '#submit-quiz' );

  function allQuestionsCompleted() {
    return Object.keys( questionValues ).length === totalQuestions;
  }

  function enableSubmit() {
    submitInput.title = 'Get your score';
    var className = 'a-btn__disabled';
    if ( submitInput.classList ) {
      submitInput.classList.remove( className );
    } else {
      submitInput.className = submitInput.className
                                         .replace( new RegExp( '(^|\\b)' +
                            className.split( ' ' )
                                     .join( '|' ) + '(\\b|$)', 'gi' ), ' ' );
    }
  }

  // thanks jQuery
  function checkOnBack( el ) {
    handleInput( el );
  }

  function handleInput( input ) {
    if ( input.name && input.checked ) {
      questionValues[input.name] = input.value;
    }

    quizComplete = allQuestionsCompleted();

    if ( quizComplete ) {
      enableSubmit();
    }
  }

  submitInput.addEventListener( 'click', function( event ) {
    if ( !quizComplete ) {
      return event.preventDefault();
    }
    return null;
  } );

  function sendEvent( action, label, category ) {
    var eventData = Analytics.getDataLayerOptions( action, label, category );
    Analytics.sendEvent( eventData );
  }

  var inputs = document.querySelectorAll( '.content_main input' );
  [].forEach.call( inputs, function( el ) {
    el.addEventListener( 'click', function( event ) {
      var input = event.target;

      if ( input.name && input.checked ) {
        questionValues[input.name] = input.value;
      }

      var action = input.getAttribute( 'data-gtm-action' );
      var label = input.getAttribute( 'data-gtm-label' );
      var category = input.getAttribute( 'data-gtm-category' );

      if ( Analytics.tagManagerIsLoaded ) {
        sendEvent( action, label, category );
      } else {
        Analytics.addEventListener( 'gtmLoaded', sendEvent );
      }

      quizComplete = allQuestionsCompleted();

      if ( quizComplete ) {
        enableSubmit();
      }
    } );
  } );
  inputs.forEach( function( input ) {
    checkOnBack( input );
  } );

} )();
