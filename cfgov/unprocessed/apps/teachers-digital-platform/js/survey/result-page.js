const Cookie = require( 'js-cookie' );
const encodeName = require( '../encode-name' );
const modals = require( '../modals' );
const initials = require( './initials' );
const { clipboardCopy } = require( '../clipboardCopy' );

const $ = document.querySelector.bind( document );
const ANSWERS_SESS_KEY = 'tdp-survey-choices';

function resultsPage() {
  modals.init();
  sessionStorage.removeItem( ANSWERS_SESS_KEY );
  Cookie.remove( 'wizard_survey_wizard' );
  initials.init();

  document.addEventListener( 'input', event => {
    const t = event.target;

    if (t.hasAttribute( 'data-initials-setter' )) {
      const fixed = String( t.value ).toUpperCase().trim().substr( 0, 3 );

      initials.update( fixed );
      $( '.share-output__copied' ).textContent = '';

      // Set value on all setters!
      const allSetters = document.querySelectorAll('[data-initials-setter]');
      [].forEach.call(allSetters, input => input.value = fixed);

      t.value = fixed;

      // Show shared URL
      const shareUrlOutput = $( '.shared-url' );
      const a = document.createElement( 'a' );
      a.href = '../view/?r=' + encodeURIComponent(
        shareUrlOutput.dataset.rparam
      );
      // href property read gives you full URL
      const shareUrl = a.href;
      shareUrlOutput.value = encodeName.encodeNameInUrl(
        shareUrl, initials.get()
      );
      $( '.share-output' ).hidden = false;
    }
  } );

  document.addEventListener( 'click', event => {
    const t = event.target;

    // Handle closing modals
    const id = t.dataset.closePrint;
    if ( id ) {
      event.stopPropagation();
      modals.close( id );
      window.print();
      return;
    }

    // Handle copying to clipboard
    if ( t === $( '.share-output__right button' ) ) {
      const shareUrl = $( '.shared-url' ).value;
      clipboardCopy( shareUrl ).then( success => {
        $( '.share-output__copied' ).textContent = success
          ? 'Link copied to clipboard.'
          : 'Copy failed. Please copy the link yourself.';
      } );
    }
  } );

  // Hide the clipboard copied message when opening share modal
  document.addEventListener( 'modal:open:before', event => {
    if ( event.detail.modal.id === 'modal-share-url' ) {
      $( '.share-output__copied' ).innerHTML = '&nbsp;';
    }
  } );

  const startOver = $( '.results-start-over' );
  if (startOver) {
    startOver.addEventListener( 'click', () => {
      Cookie.remove( 'resultUrl' );
    } );
  }
}

export { resultsPage, ANSWERS_SESS_KEY };
