import { changeElHTML, addClass, removeClass } from './dom-tools.js';

function resetFileName() {
  addClass('#file-list-wrapper', 'u-hidden');
}

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

/**
 * @param {string} fileName - A filename.
 * @returns {string} The uploaded filename.
 */
function getUploadName(fileName) {
  let uploadName = fileName;
  if (uploadName.indexOf('\\') > -1) {
    const uploadNameParts = uploadName.split('\\');
    uploadName = uploadNameParts[uploadNameParts.length - 1];
  }

  return uploadName;
}

/**
 * @param {string} fileName - The uploaded filename.
 * @returns {boolean} - True if the file is a CSV, false otherwise.
 */
function isCSV(fileName) {
  return fileName.slice(fileName.lastIndexOf('.') + 1) === 'csv';
}

export { resetFileName, resetError, setError, getUploadName, isCSV };
