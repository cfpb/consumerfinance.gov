/**
 * Copy text to clipboard
 *
 * @link https://stackoverflow.com/a/30810322/3779
 * @param {string} text
 * @returns {Promise<boolean>} Success
 */
function clipboardCopy( text ) {
  if ( !navigator.clipboard ) {
    return fallbackClipboardCopy( text );
  }

  try {
    return navigator.clipboard.writeText( text ).then(
      () => true,
      () => fallbackClipboardCopy( text ),
    );
  } catch ( err ) {
    return fallbackClipboardCopy( text );
  }
}

/**
 * Copy text to clipboard
 *
 * @link https://stackoverflow.com/a/30810322/3779
 * @param {string} text
 * @returns {Promise<boolean>} Success
 */
function fallbackClipboardCopy( text ) {
  const textArea = document.createElement( 'textarea' );
  textArea.value = text;

  // Avoid scrolling to bottom
  textArea.style.top = '0';
  textArea.style.left = '0';
  textArea.style.position = 'fixed';

  document.body.appendChild( textArea );
  textArea.focus();
  textArea.select();

  let success = false;
  try {
    success = document.execCommand( 'copy' );
  } catch ( err ) {
    // Failed
  }

  document.body.removeChild( textArea );
  return Promise.resolve(success);
}

export { clipboardCopy };

