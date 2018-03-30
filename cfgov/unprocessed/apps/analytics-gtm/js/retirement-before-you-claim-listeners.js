import $ from 'jquery';

// Retirement - Before You Claim custom analytics file

const BYCAnalytics = ( function() {
  let questionsAnswered = [],
      sliderClicks = 0,
      sliderIsActive = false,
      stepOneSubmitted = false;

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


  const delay = ( function() {
    let timer = 0;
    return function( callback, ms ) {
      clearTimeout( timer );
      timer = setTimeout( callback, ms );
    };
  } )();

  $( document ).ready( function() {

    $( '#step-one-form' ).submit( function( e ) {
      e.preventDefault();
      stepOneSubmitted = true;
      let month = $( '#bd-month' ).val(),
          day = $( '#bd-day' ).val();
      window.dataLayer.push( {
        event: 'Before You Claim Interaction',
        action: 'Get Your Estimates submit birthdate',
        label: 'Birthdate Month and Day - ' + month + '/' + day
      } );
    } );

    $( '#step-one-form' ).submit( function( e ) {
      e.preventDefault();
      let month = $( '#bd-month' ).val(),
          day = $( '#bd-day' ).val(),
          year = $( '#bd-year' ).val(),
          age = calculateAge( month, day, year );
      window.dataLayer.push( {
        event: 'Before You Claim Interaction',
        action: 'Get Your Estimates submit age',
        label: 'Age ' + age
      } );
    } );

    $( '#claim-canvas' ).on( 'mousedown', 'rect', function() {
      const age = $( this ).attr( 'data-age' );
      window.dataLayer.push( {
        event: 'Before You Claim Interaction',
        action: 'Graph Age Bar clicked',
        label: 'Age ' + age
      } );
    } );

    $( '#claim-canvas' ).on( 'mousedown', '#graph_slider-input', function() {
      sliderIsActive = true;
      sliderClicks++;
      window.dataLayer.push( {
        event: 'Before You Claim Interaction',
        action: 'Slider clicked',
        label: 'Slider clicked ' + sliderClicks + ' times'
      } );
    } );

    $( '#claim-canvas' ).on( 'click', '.age-text', function() {
      const age = $( this ).attr( 'data-age-value' );
      window.dataLayer.push( {
        event: 'Before You Claim Interaction',
        action: 'Age Text Box clicked',
        label: 'Age ' + age
      } );
    } );

    $( 'body' ).on( 'mouseup', function() {
      if ( sliderIsActive === true ) {
        const age = $( '.selected-age' ).text();
        window.dataLayer.push( {
          event: 'Before You Claim Interaction',
          action: 'Slider released',
          label: 'Age ' + age
        } );
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
        window.dataLayer.push( {
          event: 'Before You Claim Interaction',
          action: 'All Lifestyle Buttons clicked',
          label: 'All button clicks'
        } );
      }
      window.dataLayer.push( {
        event: 'Before You Claim Interaction',
        action: 'Lifestyle Button clicked',
        label: 'Question: ' + question + ' - ' + value
      } );
    } );

    $( 'input[name="benefits-display"]' ).click( function() {
      if ( stepOneSubmitted ) {
        const val = $( this ).val();
        window.dataLayer.push( {
          event: 'Before You Claim Interaction',
          action: 'Benefits View clicked',
          label: val
        } );
      }
    } );

    $( '#retirement-age-selector' ).change( function() {
      const val = $( this ).find( 'option:selected' ).val();
      window.dataLayer.push( {
        event: 'Before You Claim Interaction',
        action: 'Planned Retirement Age selected',
        label: val
      } );
    } );

    $( 'button.helpful-btn' ).click( function() {
      const val = $( this ).val();
      window.dataLayer.push( {
        event: 'Before You Claim Interaction',
        action: 'Was This Page Helpful clicked',
        label: val
      } );
    } );

    $( '[data-tooltip-target]' ).click( function() {
      const target = $( this ).attr( 'data-tooltip-target' );
      window.dataLayer.push( {
        event: 'Before You Claim Interaction',
        action: 'Tooltip clicked',
        label: 'Target: ' + target
      } );
    } );
  } );

} )( $ );
