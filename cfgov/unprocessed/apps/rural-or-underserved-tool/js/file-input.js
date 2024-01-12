import { changeElHTML, addClass, removeClass, getEl } from './dom-tools.js';

/**
 * Reset the file input value.
 */
function resetFileName() {
  getEl('#file-name').value = 'No file chosen';
}

/**
 * Set a filename for a file input.
 * @param {string} fileName - A filename.
 */
function setFileName(fileName) {
  getEl('#file-name').value = fileName;
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

export {
  resetFileName,
  setFileName,
  resetError,
  setError,
  getUploadName,
  isCSV,
};
