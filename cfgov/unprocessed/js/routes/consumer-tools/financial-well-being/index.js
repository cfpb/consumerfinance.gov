/* eslint no-global-assign: "off" */
'use strict';

var Analytics = require( '../../../modules/Analytics' );

( function() {

  var totalQuestions = 12;
  var quizComplete = false;
  var questionValues = {};
  var radioButtons = document.querySelectorAll( '[type="radio"]' );
  var submitButton = document.querySelector( '#submit-quiz' );

  function allQuestionsCompleted() {
    return Object.keys( questionValues ).length === totalQuestions;
  }

  function enableSubmit() {
    submitButton.title = 'Get your score';
    var disabledClass = 'a-btn__disabled';

    if ( submitButton.classList ) {
      submitButton.classList.remove( disabledClass );
    } else {
      // Support browsers who don't have the classList API.
      var classRegex = new RegExp( '(^|\\b)' +
                                   disabledClass.split( ' ' ).join( '|' ) +
                                   '(\\b|$)', 'gi' );
      submitButton.className = submitButton.className.replace( classRegex,
                                                               ' ' );
    }
  }

  function handleRadio( input ) {
    if ( input.name && input.checked ) {
      questionValues[input.name] = input.value;
    }

    quizComplete = allQuestionsCompleted();

    if ( quizComplete ) {
      enableSubmit();
    }
  }

  function sendEvent( action, label, category ) {
    var eventData = Analytics.getDataLayerOptions( action, label, category );
    Analytics.sendEvent( eventData );
  }

  submitButton.addEventListener( 'click', function( event ) {
    // Confirm that all questions are answered
    if ( !quizComplete ) {
      // If not, block the form submission action
      return event.preventDefault();
    }
    // Otherise, allow the form submission to go through as normal
    return null;
  } );

  [].forEach.call( radioButtons, function( el ) {
    el.addEventListener( 'click', function( event ) {
      var input = event.target;
      handleRadio( input );

      var action = input.getAttribute( 'data-gtm-action' );
      var label = input.getAttribute( 'data-gtm-label' );
      var category = input.getAttribute( 'data-gtm-category' );

      if ( Analytics.tagManagerIsLoaded ) {
        sendEvent( action, label, category );
      } else {
        Analytics.addEventListener( 'gtmLoaded', sendEvent );
      }
    } );
  } );

  // Disable submit button initially
  submitButton.classList.add( 'a-btn__disabled' );
  submitButton.title = 'Please answer all questions to get your score';

  // Look at all radios on coming back to the page or on reload
  [].forEach.call( radioButtons, function( el ) {
    handleRadio( el );
  });

} )();
