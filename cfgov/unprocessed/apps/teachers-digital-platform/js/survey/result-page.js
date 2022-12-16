import Cookies from 'js-cookie';
import clipboardCopy from 'copy-to-clipboard';
import {
  ANSWERS_SESS_KEY,
  INITIALS_LIMIT,
  RESULT_COOKIE,
  SURVEY_COOKIE,
} from './config.js';
import { encodeNameInUrl } from '../obfuscation.js';
import { init as modalsInit, close as modalsClose } from '../modals.js';
import {
  init as initialsInit,
  update as initialsUpdate,
  get as initialsGet,
} from './initials.js';

const $ = document.querySelector.bind(document);

/**
 * Initialize the results page
 */
function resultsPage() {
  modalsInit();
  sessionStorage.removeItem(ANSWERS_SESS_KEY);
  Cookies.remove(SURVEY_COOKIE);
  initialsInit();

  handleShareModal();
  handlePrintModal();
  handleResetModal();
}

/**
 * Handle initials validation and callback on valid entry.
 *
 * @param {HTMLDivElement} desc - Modal description DIV.
 * @param {Function} cb - Callback with valid initials.
 */
function withValidInitials(desc, cb) {
  const set = desc.querySelector('.tdp-survey__initials-set');
  const ini = desc.querySelector('.tdp-survey__initials');
  const err = desc.querySelector('.tdp-survey__initials-error');

  set.addEventListener('click', (event) => {
    event.preventDefault();
    if (!ini.value.trim()) {
      err.classList.add('m-notification__visible');
      return;
    }

    err.classList.remove('m-notification__visible');
    cb(ini.value);
  });

  ini.addEventListener('keyup', (event) => {
    if (event.key === 'Enter') {
      set.click();
    }
  });

  ini.addEventListener('input', () => {
    const fixed = String(ini.value)
      .toUpperCase()
      .trim()
      .substr(0, INITIALS_LIMIT);

    // Set value in both modals
    const allSetters = document.querySelectorAll('.tdp-survey__initials');
    [].forEach.call(allSetters, (input) => {
      input.value = fixed;
    });
  });
}

/**
 * Handle behavior within the share URL modal
 */
function handleShareModal() {
  const desc = $('#modal-share-url_desc');
  const shareOutput = $('.share-output');
  const copiedMsg = $('.share-output__copied');
  const a = shareOutput.querySelector('a[href]');

  // Re-hide UI changes when opening share modal
  document.addEventListener('modal:open:before', (event) => {
    if (event.detail.modal.id === 'modal-share-url') {
      $('.tdp-survey__initials-error').classList.remove(
        'm-notification__visible'
      );
      $('.share-output').hidden = true;
      $('.share-output__copied').hidden = true;
    }
  });

  withValidInitials(desc, (value) => {
    initialsUpdate(value);
    a.href =
      '../view/?r=' + encodeURIComponent(shareOutput.dataset.signedCode);
    // href property read gives you full URL
    const shareUrl = a.href;
    a.href = encodeNameInUrl(shareUrl, initialsGet());
    copiedMsg.hidden = true;
    shareOutput.hidden = false;
  });

  $('.share-output button').addEventListener('click', (event) => {
    event.preventDefault();
    clipboardCopy(a.href);
    copiedMsg.hidden = false;
  });

  a.addEventListener('click', (event) => {
    event.preventDefault();
    $('.share-output button').click();
  });
}

/**
 * Handle behavior within the print modal
 */
function handlePrintModal() {
  withValidInitials($('#modal-print_desc'), (value) => {
    initialsUpdate(value);
    modalsClose();
    window.print();
  });
}

/**
 * Handle behavior within the restart modal
 */
function handleResetModal() {
  $('#modal-reset').addEventListener('click', (event) => {
    const button = event.target.closest('[data-cancel]');
    if (button) {
      event.preventDefault();
      if (button.dataset.cancel) {
        modalsClose();
      } else {
        Cookies.remove(RESULT_COOKIE);
        location.href = $('[data-grade-select-url]').dataset.gradeSelectUrl;
      }
    }
  });
}

export { resultsPage, ANSWERS_SESS_KEY };
