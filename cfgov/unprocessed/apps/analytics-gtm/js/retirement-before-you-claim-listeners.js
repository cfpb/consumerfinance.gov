// TODO: Remove jquery.
import $ from 'jquery';

import {
  analyticsLog,
  track
} from './util/analytics-util';

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
    let now = new Date();
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

  $( document ).ready( function() {

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

    $( '#claim-canvas' ).on( 'mousedown', 'rect', function() {
      const age = $( this ).attr( 'data-age' );
      track(
        'Before You Claim Interaction',
        'Graph Age Bar clicked',
        'Age ' + age
      );
    } );

    $( '#claim-canvas' ).on( 'mousedown', '#graph_slider-input', function() {
      sliderIsActive = true;
      sliderClicks++;
      track(
        'Before You Claim Interaction',
        'Slider clicked',
        'Slider clicked ' + sliderClicks + ' times'
      );
    } );

    $( '#claim-canvas' ).on( 'click', '.age-text', function() {
      const age = $( this ).attr( 'data-age-value' );
      track(
        'Before You Claim Interaction',
        'Age Text Box clicked',
        'Age ' + age
      );
    } );

    $( 'body' ).on( 'mouseup', function() {
      if ( sliderIsActive === true ) {
        const age = $( '.selected-age' ).text();
        track(
          'Before You Claim Interaction',
          'Slider released',
          'Age ' + age
        );
        sliderIsActive = false;
      }
    } );

    $( 'button.lifestyle-btn' ).click( function() {
      const $container = $( this ).closest( '.lifestyle-question_container' );
      const question = $container.find( 'h3' ).text().trim();
      const value = $( this ).val();
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

    $( 'input[name="benefits-display"]' ).click( function() {
      if ( stepOneSubmitted ) {
        const val = $( this ).val();
        track(
          'Before You Claim Interaction',
          'Benefits View clicked',
          val
        );
      }
    } );

    $( '#retirement-age-selector' ).change( function() {
      const val = $( this ).find( 'option:selected' ).val();
      track(
        'Before You Claim Interaction',
        'Planned Retirement Age selected',
        val
      );
    } );

    $( 'button.helpful-btn' ).click( function() {
      const val = $( this ).val();
      track(
        'Before You Claim Interaction',
        'Was This Page Helpful clicked',
        val
      );
    } );

    $( '[data-tooltip-target]' ).click( function() {
      const target = $( this ).attr( 'data-tooltip-target' );
      track(
        'Before You Claim Interaction',
        'Tooltip clicked',
        'Target: ' + target
      );
    } );
  } );

} )( $ );
