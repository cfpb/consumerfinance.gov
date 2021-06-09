// TODO: remove jquery.
import $ from 'jquery';

function init() {
  const $buttons = $( '.step-two .question .lifestyle-btn' );

  $buttons.click( function() {
    const $container = $( this ).closest( '.question' );
    const respTo = $( this ).val();

    $container.find( '.lifestyle-btn' )
      .removeClass( 'lifestyle-btn__active' );
    $( this ).addClass( 'lifestyle-btn__active' );

    $container.find( '.lifestyle-img' ).slideUp();
    $container.find( '.lifestyle-response' )
      .not( '[data-responds-to="' + respTo + '"]' ).slideUp();
    const selector = '.lifestyle-response[data-responds-to="' + respTo + '"]';
    $container.find( selector ).slideDown();

    $container.attr( 'data-answered', 'yes' );

  } );
}

/* This function updates the text in the "questions" in Step 2
    based on the user's current age
    @param {number} currentAge   The user's current age */
function update( currentAge ) {
  const $ageSplits = $( '.lifestyle-btn.age-split' );
  if ( currentAge < 50 ) {
    $ageSplits.each( function() {
      $( this ).val(
        $( this ).attr( 'data-base-value' ) + '-under50'
      );
    } );
  } else {
    $ageSplits.each( function() {
      $( this ).val(
        $( this ).attr( 'data-base-value' ) + '-over50'
      );
    } );
  }
}

export default {
  init,
  update
};
