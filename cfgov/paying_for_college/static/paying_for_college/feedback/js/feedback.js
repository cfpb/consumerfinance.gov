const feedbackContainer = document.querySelector( '#feedback-container' );
const feedbackButton = feedbackContainer.querySelector( 'button' );
const feedbackTextarea = feedbackContainer.querySelector( 'textarea' );
feedbackButton.setAttribute( 'disabled', 'disabled' );
feedbackTextarea.addEventListener( 'keyup' , feedbackTextareaKeyUp );

function feedbackTextareaKeyUp( event ) {
    if ( event.target.value === '' ) {
        feedbackButton.setAttribute( 'disabled', 'disabled' );
    } else {
        feedbackButton.removeAttribute( 'disabled' );
    }
}
