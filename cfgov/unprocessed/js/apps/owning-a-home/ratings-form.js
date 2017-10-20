'use strict';


function init() {
  const ratingsForm = document.querySelector( '.oah-ratings-form' );
  const ratingsInputs = ratingsForm.querySelectorAll( '.rating-inputs input' );
  const ratingsInputsLength = ratingsInputs.length;
  const feedBackLinkElement = ratingsForm.querySelector( '.feedback-link' );
  const feedBackLinkHref = feedBackLinkElement.getAttribute( 'href' );
  const ratingsMsgElement = ratingsForm.querySelector( '.rating-message' );

  function _onChange( e ) {
    ratingsMsgElement.classList.add( 'visible' );

    if ( feedBackLinkHref ) {
      feedBackLinkElement.setAttribute(
        'href',
        feedBackLinkHref + '?is_helpful=' + e.target.value
      );
    }

    for ( let i = 0; i < ratingsInputsLength; i++ ) {
      ratingsInputs[i].setAttribute( 'disabled', true );
    }
  }

  for ( let i = 0; i < ratingsInputsLength; i++ ) {
    ratingsInputs[i].addEventListener( 'change', _onChange );
  }
}

module.exports = { init: init };
