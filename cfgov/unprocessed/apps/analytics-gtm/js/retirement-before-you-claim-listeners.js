// TODO: Remove jquery.
import $ from 'jquery';

import { track } from './util/analytics-util';

// Retirement - Before You Claim custom analytics file

const BYCAnalytics = ( function() {

  const questionsAnswered = [];
  let sliderClicks = 0;
  let sliderIsActive = false;
  let stepOneSubmitted = false;

  function calculateAge( month, day, year, currentDate ) {
    let now = currentDate;
    if ( currentDate instanceof Date !== true ) {
      now = new Date();
    }
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

    $( '#step-one-form' ).submit( function( e ) {
      e.preventDefault();
      stepOneSubmitted = true;
      let month = $( '#bd-month' ).val(),
          day = $( '#bd-day' ).val();
      track(
        'Before You Claim Interaction',
        'Get Your Estimates submit birthdate',
        'Birthdate Month and Day - ' + month + '/' + day
      );
    } );

    $( '#step-one-form' ).submit( function( e ) {
      e.preventDefault();
      let month = $( '#bd-month' ).val(),
          day = $( '#bd-day' ).val(),
          year = $( '#bd-year' ).val(),
          age = calculateAge( month, day, year );
      track(
        'Before You Claim Interaction',
        'Get Your Estimates submit age',
        'Age ' + age
      );
    } );

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
      let $container = $( this ).closest( '.lifestyle-question_container' ),
          question = $container.find( 'h3' ).text().trim(),
          value = $( this ).val();
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
