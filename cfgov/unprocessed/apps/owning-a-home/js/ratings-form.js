/**
 * Initialize the ratings form for Buying a House.
 */
function init() {
  const ratingsForm = document.querySelector( '.oah-ratings-form' );
  const ratingsInputs = ratingsForm.querySelectorAll( '.rating-inputs input' );
  const ratingsInputsLength = ratingsInputs.length;
  const feedBackLinkElement = ratingsForm.querySelector( '.feedback-link' );
  const feedBackLinkHref = feedBackLinkElement.getAttribute( 'href' );
  const ratingsMsgElement = ratingsForm.querySelector( '.rating-message' );

  /**
   * Handle a change of the rating inputs.
   * @param {Event} event - The onChange event object.
   */
  function _onChange( event ) {
    ratingsMsgElement.classList.add( 'visible' );

    if ( feedBackLinkHref ) {
      feedBackLinkElement.setAttribute(
        'href',
        feedBackLinkHref + '?is_helpful=' + event.target.value
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

export { init };
