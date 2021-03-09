import {
  analyticsLog,
  track
} from './util/analytics-util';

import { closest } from '@cfpb/cfpb-atomic-component/src/utilities/dom-traverse.js';

// Retirement - Before You Claim custom analytics file

const BYCAnalytics = ( function() {

  const questionsAnswered = [];
  let sliderClicks = 0;
  let sliderIsActive = false;
  let stepOneSubmitted = false;

  /**
   * @param {number} month - Month of birth.
   * @param {number} day - Day of birth.
   * @param {number} year - Year of birth.
   * @returns {number} The age, in years, based on current date.
   */
  function calculateAge( month, day, year ) {
    const now = new Date();
    const birthdate = new Date( year, Number( month ) - 1, day );
    let age = now.getFullYear() - birthdate.getFullYear();
    const m = now.getMonth() - birthdate.getMonth();
    if ( m < 0 || ( m === 0 && now.getDate() < birthdate.getDate() ) ) {
      age--;
    }
    if ( isNaN( age ) ) {
      return false;
    }
    return age;
  }

  const stepOneForm = document.querySelector( '#step-one-form' );
  stepOneForm.addEventListener( 'submit', formSubmitted );

  /**
   * Handle submission of the form.
   * @param {Event} evt - Form submit event object.
   */
  function formSubmitted( evt ) {
    evt.preventDefault();
    stepOneSubmitted = true;

    // Track birthdate.
    const month = document.querySelector( '#bd-month' ).value;
    const day = document.querySelector( '#bd-day' ).value;
    track(
      'Before You Claim Interaction',
      'Get Your Estimates submit birthdate',
      'Birthdate Month and Day - ' + month + '/' + day
    );

    // Track age.
    const year = document.querySelector( '#bd-year' ).value;
    const age = calculateAge( month, day, year );
    track(
      'Before You Claim Interaction',
      'Get Your Estimates submit age',
      'Age ' + age
    );

    // Start mouseflow heatmap capture.
    if ( window.mouseflow ) {
      // Stop any in-progress heatmap capturing.
      window.mouseflow.stop();
      // Start a new heatmap recording.
      window.mouseflow.start();
      analyticsLog( 'Mouseflow capture started!' );
    }
  }

  document.querySelector( '#claim-canvas' ).addEventListener( 'mousedown', function( event ) {
    if ( event.target.classList.contains( 'graph__bar' ) ) {
      const age = event.target.getAttribute( 'data-bar_age' );
      track(
        'Before You Claim Interaction',
        'Graph Age Bar clicked',
        'Age ' + age
      );
    }
  } );

  document.querySelector( '#graph_slider-input' ).addEventListener( 'mousedown', function() {
    sliderIsActive = true;
    sliderClicks++;
    track(
      'Before You Claim Interaction',
      'Slider clicked',
      'Slider clicked ' + sliderClicks + ' times'
    );
  } );

  document.querySelector( '#claim-canvas' ).addEventListener( 'click', function( event ) {
    const target = event.target.parentNode;
    if ( target.classList.contains( 'age-text' ) ) {
      const age = target.getAttribute( 'data-age-value' );
      track(
        'Before You Claim Interaction',
        'Age Text Box clicked',
        'Age ' + age
      );
    }
  } );

  document.body.addEventListener( 'mouseup', function() {
    if ( sliderIsActive === true ) {
      const age = document.querySelector( '.selected-age' ).innerText;
      track(
        'Before You Claim Interaction',
        'Slider released',
        'Age ' + age
      );
      sliderIsActive = false;
    }
  } );

  const lifestyleBtns = document.querySelectorAll( 'button.lifestyle-btn' );
  for ( let i = 0, len = lifestyleBtns.length; i < len; i++ ) {
    lifestyleBtns[i].addEventListener( 'click', function( event ) {
      const target = event.currentTarget;
      // TODO: migrate off closest requirement, if possible.
      const $container = closest( target, '.lifestyle-question_container' );
      const question = $container.querySelector( 'h3' ).innerText.trim();
      const value = target.value;
      if ( questionsAnswered.indexOf( question ) === -1 ) {
        questionsAnswered.push( question );
      }
      if ( questionsAnswered.length === 5 ) {
        track(
          'Before You Claim Interaction',
          'All Lifestyle Buttons clicked',
          'All button clicks'
        );
      }
      track(
        'Before You Claim Interaction',
        'Lifestyle Button clicked',
        'Question: ' + question + ' - ' + value
      );
    } );
  }

  const benefitsRadios = document.querySelectorAll( 'input[name="benefits-display"]' );
  for ( let i = 0, len = benefitsRadios.length; i < len; i++ ) {
    // eslint-disable-next-line no-loop-func
    benefitsRadios[i].addEventListener( 'click', function( event ) {
      if ( stepOneSubmitted ) {
        const val = event.currentTarget.value;
        track(
          'Before You Claim Interaction',
          'Benefits View clicked',
          val
        );
      }
    } );
  }

  document.querySelector( '#retirement-age-selector' ).addEventListener( 'change', function( event ) {
    const target = event.currentTarget;
    const val = target[target.selectedIndex].value;
    track(
      'Before You Claim Interaction',
      'Planned Retirement Age selected',
      val
    );
  } );

  const helpfulBtns = document.querySelectorAll( 'button.helpful-btn' );
  for ( let i = 0, len = helpfulBtns.length; i < len; i++ ) {
    helpfulBtns[i].addEventListener( 'click', function( event ) {
      const val = event.currentTarget.value;
      track(
        'Before You Claim Interaction',
        'Was This Page Helpful clicked',
        val
      );
    } );
  }

  document.querySelector( '[data-tooltip-target]' ).addEventListener( 'click', function( event ) {
    const target = event.currentTarget.getAttribute( 'data-tooltip-target' );
    track(
      'Before You Claim Interaction',
      'Tooltip clicked',
      'Target: ' + target
    );
  } );

} )();
