import { changeElHTML, addClass, removeClass } from './dom-tools.js';

/**
 * Clear errors.
 */
function resetError() {
  addClass('#file-error', 'u-hidden');
  addClass('#process-error', 'u-hidden');
  changeElHTML('.js-error-message', '');
}

/**
 * Display an error message.
 * @param {string} message - An error message.
 */
function setError(message) {
  changeElHTML('#file-error-desc', message);
  removeClass('#file-error', 'u-hidden');
}

export { resetError, setError };
