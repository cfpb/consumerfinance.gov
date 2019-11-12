import { closest } from '../../../js/modules/util/dom-traverse';
import {
  getElementHeight,
  getYLocation,
  hide,
  isVisible,
  show,
  slide
} from './repay-utils';

const decisionStackerTargets = {
  '0':  { 'question': '1', 'federal': 'a', 'non-federal': 'b', 'both': 'c' },
  '1a': { question: '2', yes: 'a', no: 'b' },
  '1b': { question: '2', yes: 'c', no: 'd' },
  '2a': { 'question': '3', 'yes': 'a', 'no': 'b', 'not-sure': 'b' },
  '2b': { 'question': '8', 'yes': 'a', 'no': 'b', 'not-sure': 'b' },
  '2c': { 'question': '3', 'yes': 'c', 'no': 'd', 'not-sure': 'd' },
  '2d': { 'question': '8', 'yes': 'c', 'no': 'd', 'not-sure': 'd' },
  '3a': { question: '4', yes: 'a', no: 'b' },
  '3b': { 'question': '8', 'yes': 'a', 'no': 'b', 'not-sure': 'b' },
  '3c': { module: 'm12' },
  '3d': { 'question': '8', 'yes': 'c', 'no': 'e', 'not-sure': 'e' },
  '4a': { question: '5', yes: 'a', no: 'b' },
  '4b': { module: 'm5' },
  '5a': { module: 'm4' },
  '5b': { question: '6', yes: 'a', no: 'b' },
  '6a': { module: 'm5', yes: 'a', no: 'b' },
  '6b': { question: '7', yes: 'a', no: 'b' },
  '7a': { module: 'm6' },
  '7b': { module: 'm7' },
  '8a': { question: '9', yes: 'a', no: 'b' },
  '8b': { question: '9', yes: 'a', no: 'c' },
  '8c': { question: '9', yes: 'e', no: 'd' },
  '8d': { question: '9', yes: 'e', no: 'g' },
  '8e': { question: '9', yes: 'f', no: 'g' },
  '9a': { module: 'm2' },
  '9b': { module: 'm1' },
  '9c': { module: 'm3' },
  '9d': { module: 'm9' },
  '9e': { module: 'm10' },
  '9f': { module: 'm13' },
  '9g': { module: 'm11' }
}; // end decisionStackerTargets

const decisionStacker = function( appElement, targets ) {
  const stacker = {};
  stacker.appElement = appElement;
  const writingHash = true;

  const assignButtons = function( code ) {
    // this function relies on decisionStackerTargets object
    if ( typeof targets !== 'object' ) {
      return false;
    }
    if ( targets[code].hasOwnProperty( 'question' ) ) {
      const elem = document.querySelector( '#q' + targets[code].question );
      const sectionOrigin = elem.getAttribute( 'data-ds-origin' );
      const sectionData = targets[sectionOrigin];
      const buttons = elem.querySelectorAll( 'button' );
      buttons.forEach( button => {
        const name = button.getAttribute( 'data-ds-name' );
        if ( sectionData.hasOwnProperty( name ) ) {
          button.value = sectionData.question + sectionData[name];
        }
      } );
    }
    return true;
  };

  const initializeButtons = () => {
    const buttons = appElement.querySelectorAll( '.ds-section .ds-buttons button' );

    buttons.forEach( button => {
      button.addEventListener( 'click', event => {
        const button = event.target;
        const code = button.value;
        const destinationObject = decisionStackerTargets[code];
        let destination;
        let destinationElement;

        if ( writingHash === true ) {
          if ( location.hash !== '' ) {
            location.hash += ':';
          }
          location.hash += button.getAttribute( 'data-ds-name' );
        }

        // destination is a question
        if ( destinationObject.hasOwnProperty( 'question' ) ) {
          destination = '#q' + destinationObject.question;
        } else {
          // destination is a module
          destination = '#' + destinationObject.module;
          show( document, '.ds-clear-all.ds-clear-after-m' );
        }

        // Find and modify destination element
        destinationElement = document.querySelector( destination );
        destinationElement.setAttribute( 'data-ds-origin', code );

        slide( 'down', destinationElement );

        const section = closest( button, '.ds-section' );
        const name = button.getAttribute( 'data-ds-name' );
        const respSelector = '[data-responds-to="' + name + '"]';

        section.setAttribute( 'data-ds-decision', name );
        assignButtons( code );
        slide( 'up', section.querySelector( '.ds-content' ) );
        console.log( 'selresp: ', section, respSelector );
        slide( 'down', section.querySelector( '.ds-response-container' ) );
        show( section, respSelector );
        show( document, '.ds-clear-all.ds-clear-after-q' );

        // scrollToDestination( destinationElement );

      } );

    } );

    const init = () => {
      assignButtons( 0 );
      initializeButtons();
    };

    // Initialize the "Edit" buttons
    const editButtons = appElement.querySelectorAll( '.ds-response-container .go-back' );
    editButtons.forEach( button => {
      button.addEventListener( 'click', event => {

        const button = event.target;
        const section = closest( button, '.ds-section' );
        const questionNumber = Number( section.getAttribute( 'data-ds-qnum' ) );
        const questions = document.querySelectorAll( '.ds-question' );
        let hash = '';

        // Only check visible elements
        const visibleQuestions = Array.prototype.slice.call( questions ).filter( isVisible );

        visibleQuestions.forEach( ( questionSection, i ) => {
          const thisNumber = Number( questionSection.getAttribute( 'data-ds-qnum' ) );

          console.log( 'thisNumber', thisNumber, 'questionNumber', questionNumber );
          if ( thisNumber > questionNumber ) {
            /* slide( 'up', questionSection.querySelector( '.ds-content' ) );
               slide( 'up', questionSection.querySelector( '.ds-response-container' ) ); */
            hide( questionSection );
          } else if ( thisNumber === questionNumber ) {
            slide( 'up', questionSection.querySelector( '.ds-response-container' ) );
            hide( section, '[data-responds-to]' );
            slide( 'down', questionSection.querySelector( '.ds-content' ) );
          } else if ( thisNumber < questionNumber ) {
            // rebuild hash
            if ( i !== 0 ) {
              hash += '`:';
            }
            hash += questionSection.getAttribute( 'data-ds-decision' );
          }
        } );

        hide( document, '.ds-module' );

        // hide clear all when user is on Question #1
        if ( questionNumber === 1 ) {
          hide( document, '.ds-clear-all' );
        }
        // reset hash
        location.hash = hash;

        // scrollToDestination( section );
      } );
    } );

    document.querySelector( '.ds-clear-button' )
      .addEventListener( 'click', event => {
        document.querySelector( '#q1 .go-back' ).click();
      } );

  };

  const processHash = position => {
    const hashes = location.hash.replace( '#', '' ).split( ':' );
    const selector = '.ds-buttons:visible button[data-ds-name="' + hashes[position] + '"]';

    document.querySelectorAll( selector ).forEach( button => {
      if ( isVisible( button ) ) {
        button.addEventListener( 'click', () => {
          if ( position + 1 < hashes.length ) {
            processHash( position + 1 );
          }
        } );
      }
    } );
  };

  const scroll = function( destination ) {
    const scrollTop = destination.offsetTop - 50;

    if ( window.pageYOffset >= scrollTop ) return;

    const duration = 500;
    const start = window.pageYOffset;
    const startTime = new Date().getTime();

    const now = new Date().getTime();
    const time = Math.min( 1, ( now - startTime ) / duration );
    const newOffset = Math.ceil( time * time * ( scrollTop - start ) ) + start;
    window.scroll( 0, newOffset );

    requestAnimationFrame( scroll );
  };

  const scrollToDestination = destination => {
    const scrollTop = destination.offsetTop - 50;
    if ( 'requestAnimationFrame' in window === false ) {
      window.scrollTo( 0, scrollTop );
    } else {
      scroll( destination );
    }
  };

  // init();

  return stacker;
};


const init = function() {
  const dsSections = document.querySelectorAll( '.ds-section' );
  dsSections.forEach( section => {
    const stacker = decisionStacker( section, decisionStackerTargets );
  } );
};


if ( 'replaceState' in window.history ) {
  window.addEventListener( 'load', init );
}

/* document.addEventListener( 'DOMContentLoaded', ( event ) => {
   console.log( 'LOAD' ); */

/* const dsSections = document.querySelectorAll( '.ds-section' );
   dsSections.forEach( ( section ) => {
   let stacker = decisionStacker( section, decisionStackerTargets );
   console.log( 'Hi' );
   }) */

// } );

