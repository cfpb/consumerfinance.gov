const feedbackContainer = document.querySelector( '#feedback-container' );
const feedbackButton = feedbackContainer.querySelector( 'button' );
const feedbackTextarea = feedbackContainer.querySelector( 'textarea' );
feedbackButton.setAttribute( 'disabled', 'disabled' );
feedbackTextarea.addEventListener( 'keyup', feedbackTextareaKeyUp );

/**
 * Disable the submit button if there is no content in the textarea input.
 * @param {KeyboardEvent} event - The keyup event object from the textarea.
 */
function feedbackTextareaKeyUp( event ) {
  if ( event.target.value === '' ) {
    feedbackButton.setAttribute( 'disabled', 'disabled' );
  } else {
    feedbackButton.removeAttribute( 'disabled' );
  }
}
