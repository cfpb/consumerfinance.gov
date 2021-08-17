const Cookie = require( 'js-cookie' );
const { ANSWERS_SESS_KEY, RESULT_COOKIE, SURVEY_COOKIE } = require( './config' );
const encodeName = require( '../encode-name' );
const modals = require( '../modals' );
const initials = require( './initials' );
const { clipboardCopy } = require( '../clipboardCopy' );

const $ = document.querySelector.bind( document );

/**
 * Initialize the results page
 */
function resultsPage() {
  modals.init();
  sessionStorage.removeItem( ANSWERS_SESS_KEY );
  Cookie.remove( SURVEY_COOKIE );
  initials.init();

  handleShareModal();
  handlePrintModal();

  // Re-hide UI changes when opening share modal
  document.addEventListener( 'modal:open:before', () => {
    $( '.tdp-survey__initials-error' ).classList.remove( 'm-notification__visible' );
    $( '.share-output' ).hidden = true;
    $( '.share-output__copied' ).hidden = true;
  } );

  const startOver = $( '.results-start-over' );
  if ( startOver ) {
    startOver.addEventListener( 'click', () => {
      Cookie.remove( RESULT_COOKIE );
    } );
  }
}

/**
 * Handle initials validation and callback on valid entry
 *
 * @param {HTMLDivElement} desc Modal description DIV
 * @param {function} cb Callback with valid initials
 */
function withValidInitials( desc, cb ) {
  const set = desc.querySelector( '.tdp-survey__initials-set' );
  const ini = desc.querySelector( '.tdp-survey__initials' );
  const err = desc.querySelector( '.tdp-survey__initials-error' );

  set.addEventListener( 'click', event => {
    event.preventDefault();
    if ( ini.value.trim() ) {
      err.classList.remove( 'm-notification__visible' );
      return cb( ini.value );
    } else {
      err.classList.add( 'm-notification__visible' );
    }
  } );

  ini.addEventListener( 'keyup', event => {
    if ( event.key === 'Enter' ) {
      set.click();
    }
  } );

  ini.addEventListener( 'input', () => {
    const fixed = String( ini.value ).toUpperCase().trim().substr( 0, 3 );

    // Set value in both modals
    const allSetters = document.querySelectorAll( '.tdp-survey__initials' );
    [].forEach.call( allSetters, input => {
      input.value = fixed;
    } );
  } );
}

/**
 * Handle behavior within the share URL modal
 */
function handleShareModal() {
  const desc = $( '#modal-share-url_desc' );
  const shareOutput = $( '.share-output' );
  const copiedMsg = $( '.share-output__copied' );
  const a = shareOutput.querySelector( 'a[href]' );
  if ( !desc || !shareOutput || !a || !copiedMsg ) {
    return;
  }

  withValidInitials( desc, value => {
    initials.update( value );
    a.href = '../view/?r=' + encodeURIComponent(
      shareOutput.dataset.rparam
    );
    // href property read gives you full URL
    const shareUrl = a.href;
    a.href = encodeName.encodeNameInUrl(
      shareUrl, initials.get()
    );
    copiedMsg.hidden = true;
    shareOutput.hidden = false;
  } );

  $( '.share-output button' ).addEventListener( 'click', event => {
    event.preventDefault();
    clipboardCopy( a.href ).then( () => {
      copiedMsg.hidden = false;
    } );
  } );

  a.addEventListener( 'click', event => {
    event.preventDefault();
    $( '.share-output button' ).click();
  } );
}

/**
 * Handle behavior within the print modal
 */
function handlePrintModal() {
  const desc = $( '#modal-print_desc' );
  if ( !desc ) {
    return;
  }

  withValidInitials( desc, value => {
    initials.update( value );
    modals.close( 'modal-print' );
    window.print();
  } );
}

export { resultsPage, ANSWERS_SESS_KEY };
