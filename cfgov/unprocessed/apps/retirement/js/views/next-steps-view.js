import isElementInView from '../utils/is-element-in-view';

// TODO: remove jquery.
import $ from 'jquery';

let currentAge = 0;
let fullAge = 0;

function init( ageRightNow, fullRetirementAge ) {
  currentAge = ageRightNow;
  fullAge = fullRetirementAge;

  limitAgeSelector( currentAge );

  $( '#retirement-age-selector' ).change( function() {
    chooseClaimingAge();
  } );

  $( '#age-selector-response .helpful-btn' ).click( function() {
    feedbackButton();
  } );
}

/* This function updates the text in Step 3
    based on the user's chosen retirement age
    @param {number} fullAge   The user's full retirement age */
function chooseClaimingAge() {

  if ( $( '#retirement-age-selector' ).find(
    'option:selected'
  ).val() === '' ) {
    $( '#age-selector-response' ).hide();
  } else {
    const age = parseInt(
      $( '#retirement-age-selector' ).find( 'option:selected' ).val(), 10
    );

    $( '.next-step-description' ).hide();
    $( '.next-steps .step-two_option' ).hide();
    $( '#age-selector-response' ).show();
    $( '#age-selector-response .age-response-value' ).text( age );

    if ( age < fullAge ) {
      $( '.next-steps_under' ).show();
    } else if ( age === fullAge ) {
      $( '.next-steps_equal' ).show();
    } else if ( age === 70 ) {
      $( '.next-steps_max' ).show();
    } else {
      $( '.next-steps_over' ).show();
    }

    // Scroll response into view if it's not visible
    if ( isElementInView( '#age-selector-response' ) === false ) {
      $( 'html, body' ).animate( {
        scrollTop: $( '#retirement-age-selector' ).offset().top - 20
      }, 300 );
    }
  }

}

/* This function limits the age selector in Step 3 to
    the user's current age or higher
    @param {number} currentAge   The user's current age */
function limitAgeSelector( currentAge ) {
  const $select = $( '#retirement-age-selector' );
  const firstOption = $select.find( 'option' )[0];
  let retirementAge = 62;

  $select.empty();
  // We save and append the first OPTION, "Choose age"
  $select.append( firstOption );
  if ( retirementAge < currentAge ) {
    retirementAge = currentAge;
  }

  for ( let x = retirementAge; x <= 70; x++ ) {
    let elem = '<option value="' + x;
    elem += '">' + x + '</option>';
    $select.append( elem );
  }
}

/* This function defines the feedback button interactions in Step 3. */
function feedbackButton() {
  $( '#age-selector-response .thank-you' ).show();
  $( '#age-selector-response .helpful-btn' )
    .attr( 'disabled', true )
    .addClass( 'btn__disabled' ).hide();
}

export default {
  init
};
