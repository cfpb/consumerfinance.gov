import DT from './dom-tools';

/**
 * Reset the file input value.
 */
function resetFileName() {
  DT.getEl( '#file-name' ).value = 'No file chosen';
}

/**
 * Set a filename for a file input.
 * @param {string} fileName - A filename.
 */
function setFileName( fileName ) {
  DT.getEl( '#file-name' ).value = fileName;
}

/**
 * Clear errors.
 */
function resetError() {
  DT.addClass( '#file-error', 'u-hidden' );
  DT.addClass( '#process-error', 'u-hidden' );
  DT.changeElHTML( '.js-error-message', '' );
}

/**
 * Display an error message.
 * @param {string} message - An error message.
 */
function setError( message ) {
  DT.changeElHTML( '#file-error-desc', message );
  DT.removeClass( '#file-error', 'u-hidden' );
}

/**
 * @param {string} fileName - A filename.
 * @returns {string} The uploaded filename.
 */
function getUploadName( fileName ) {
  let uploadName = fileName;
  if ( uploadName.indexOf( '\\' ) > -1 ) {
    const uploadNameParts = uploadName.split( '\\' );
    uploadName = uploadNameParts[uploadNameParts.length - 1];
  }

  return uploadName;
}

/**
 * @param {string} fileName The uploaded filename.
 * @returns {boolean} - True if the file is a CSV, false otherwise.
 */
function isCSV( fileName ) {
  return fileName.substr( fileName.lastIndexOf( '.' ) + 1 ) === 'csv';
}


export default {
  resetFileName,
  setFileName,
  resetError,
  setError,
  getUploadName,
  isCSV
};
