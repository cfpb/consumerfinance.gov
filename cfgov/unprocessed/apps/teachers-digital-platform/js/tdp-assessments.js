const encodeName = require('./encode-name');

const assessments = {
  init: () => {
    const $ = document.querySelector.bind(document);

    if (!$('.tdp-assessment-results')) {
      return;
    }

    const showInitials = $('.show-initials');
    if (showInitials) {
      const initials = encodeName.decodeNameFromUrl(location.href);
      if (initials) {
        showInitials.querySelector('strong').textContent = initials;
      }
      showInitials.hidden = false;
    }

    const shareForm = $('.share-url-form');
    if (shareForm) {
      const input = $('.share-customize [name=initials]');
      input.value = encodeName.recallName() || '';

      shareForm.addEventListener('submit', e => {
        e.preventDefault();
        const initials = $('.share-customize [name=initials]').value.trim();
        if (initials) {
          encodeName.storeName(initials);
        } else {
          encodeName.forgetName();
        }
        const output = $('.shared-url');
        const a = document.createElement('a');
        a.href = '../show/?r=' + encodeURIComponent(output.dataset.rparam);
        // Read property gives you full URL
        const shareUrl = a.href;
        output.value = encodeName.encodeNameInUrl(shareUrl, initials);
        $('.share-output').hidden = false;
      });
    }
  }
};

module.exports = assessments;
