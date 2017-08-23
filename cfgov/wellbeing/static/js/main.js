/* eslint no-global-assign: "off" */
'use strict';

( function() {

  function serialize(form){if(!form||form.nodeName!=="FORM"){return }var i,j,q=[];for(i=form.elements.length-1;i>=0;i=i-1){if(form.elements[i].name===""){continue}switch(form.elements[i].nodeName){case"INPUT":switch(form.elements[i].type){case"text":case"hidden":case"password":case"button":case"reset":case"submit":q.push(form.elements[i].name+"="+encodeURIComponent(form.elements[i].value));break;case"checkbox":case"radio":if(form.elements[i].checked){q.push(form.elements[i].name+"="+encodeURIComponent(form.elements[i].value))}break;case"file":break}break;case"TEXTAREA":q.push(form.elements[i].name+"="+encodeURIComponent(form.elements[i].value));break;case"SELECT":switch(form.elements[i].type){case"select-one":q.push(form.elements[i].name+"="+encodeURIComponent(form.elements[i].value));break;case"select-multiple":for(j=form.elements[i].options.length-1;j>=0;j=j-1){if(form.elements[i].options[j].selected){q.push(form.elements[i].name+"="+encodeURIComponent(form.elements[i].options[j].value))}}break}break;case"BUTTON":switch(form.elements[i].type){case"reset":case"submit":case"button":q.push(form.elements[i].name+"="+encodeURIComponent(form.elements[i].value));break}break}}return q.join("&")};

  if ( !document.querySelector( '#submit-quiz' ) ) return;

  var scoring = {
    'read-self': {
      '18-61': [
        14, 19, 22, 25, 27, 29, 31, 32, 34, 35, 37, 38, 40, 41, 42, 44, 45, 46,
        47, 49, 50, 51, 52, 54, 55, 56, 58, 59, 60, 62, 63, 65, 66, 68, 69, 71,
        73, 75, 78, 81, 86
      ],
      '62-plus': [
        14, 20, 24, 26, 29, 31, 33, 35, 36, 38, 39, 41, 42, 44, 45, 46, 48, 49,
        50, 52, 53, 54, 56, 57, 58, 60, 61, 63, 64, 66, 67, 69, 71, 73, 75, 77,
        79, 82, 84, 88, 95
      ]
    },
    'read-to-me': {
      '18-61': [
        16, 21, 24, 27, 29, 31, 33, 34, 36, 38, 39, 40, 42, 43, 44, 45, 47, 48,
        49, 50, 52, 53, 54, 55, 57, 58, 59, 60, 62, 63, 65, 66, 68, 70, 71, 73,
        76, 78, 81, 85, 91
      ],
      '62-plus': [
        18, 23, 26, 28, 30, 32, 33, 35, 36, 38, 39, 40, 41, 43, 44, 45, 46, 47,
        48, 49, 50, 52, 53, 54, 55, 56, 57, 58, 60, 61, 62, 64, 65, 67, 68, 70,
        72, 75, 77, 81, 87
      ]
    }
  };

  var totalQuestions = 12;
  var quizComplete = false;
  var questionValues = {};

  function allQuestionsCompleted() {
    return Object.keys( questionValues ).length === totalQuestions;
  }

  function enableSubmit() {
    var submitInput = document.querySelector( '#submit-quiz' );
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

// $( document ).ready( function() {
  var submitInput = document.querySelector( '#submit-quiz' );
  submitInput.addEventListener( 'click', function( event ) {
    if ( !quizComplete ) {
      return event.preventDefault();
    }
    return null;
  } );
// } );

  var quizForm = document.querySelector( '#quiz-form' );
  quizForm.addEventListener( 'submit', function( event ) {
    event.preventDefault();
    var formValues = {};
    var pathname = window.location.pathname;
    var resultsPagePath = '';

    if ( pathname.match( 'index.html' ) ) {
      resultsPagePath = pathname.replace( 'index.html', 'results/?' );
    } else if ( pathname.match( 'alt' ) ) {
      /* temporary condition for testing */
      resultsPagePath = pathname + 'results-alt/?';
    } else {
      resultsPagePath = pathname + 'results/?';
    }

    var serializedForm = serialize( quizForm );
    serializedForm.split( '&' ).forEach( function( v ) {
      var keyval = v.split( '=' );
      formValues[keyval[0]] = keyval[1];
    } );

    window.location = resultsPagePath +
      scoring[formValues.method][formValues.age][
        Object.keys( formValues ).filter( function( key ) {
          return key.indexOf( 'quest' ) === 0;
        } ).reduce( function( a, b ) {
          return a + Number( formValues[b] );
        }, 0 )
      ];
  } );

  var inputs = document.querySelectorAll( '.content_main input' );
  [].forEach.call( inputs, function( el ) {
    el.addEventListener( 'click', function( event ) {
      var input = event.target;

      if ( input.name && input.checked ) {
        questionValues[input.name] = input.value;
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
