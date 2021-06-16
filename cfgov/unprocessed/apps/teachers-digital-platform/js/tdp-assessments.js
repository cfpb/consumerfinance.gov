const Cookie = require( 'js-cookie' );
const encodeName = require( './encode-name' );
const ChoiceField = require( './assess/ChoiceField' );

const $ = document.querySelector.bind( document );

const assessments = {
  init: () => {
    const answersSessionKey = 'tdp-assess-choices';

    if ($( '.tdp-assessment-results' )) {
      sessionStorage.removeItem( answersSessionKey );

      const showInitials = $( '.show-initials' );
      if (showInitials) {
        // Show initials encoded in URL hash
        const initials = encodeName.decodeNameFromUrl( location.href );
        if (initials) {
          showInitials.querySelector( 'strong' ).textContent = initials;
          showInitials.hidden = false;
        }
      }

      const shareForm = $( '.share-url-form' );
      if (shareForm) {
        // Create share URL and show input once initials are entered
        shareForm.addEventListener( 'submit', e => {
          e.preventDefault();

          // Create URL with initials
          const initials = $( '.share-customize [name=initials]' ).value.trim();
          const output = $( '.shared-url' );
          const a = document.createElement( 'a' );
          a.href = '../show/?r=' + encodeURIComponent( output.dataset.rparam );
          // Read property gives you full URL
          const shareUrl = a.href;
          output.value = encodeName.encodeNameInUrl( shareUrl, initials );
          $( '.share-output' ).hidden = false;
        } );
      }
    }

    if ($( '.tdp-assessment-intro' )) {
      // Entry links clear session before entry
      const link = $( '.assess-entry-link' );

      function forgetEverything() {
        Cookie.remove( 'resultUrl' );
        Cookie.remove( 'wizard_assessment_wizard' );
        sessionStorage.removeItem( answersSessionKey );
      }

      link.addEventListener( 'click', forgetEverything );
      link.addEventListener( 'mouseover', forgetEverything );
    }

    if ($( '.tdp-assessment-page' )) {
      ChoiceField.init();
      const store = ChoiceField.restoreFromSession( answersSessionKey );
      ChoiceField.watchAndStore( answersSessionKey, store );
    }
  }
};

module.exports = assessments;
