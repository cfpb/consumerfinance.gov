/**
 * Formats a raw URL to be used in an href attribute.
 * The raw URL may or may not start with "http://" or "https://"
 * @param  {string} url The raw URL
 * @returns {string} The formated URL
 */
function formatSchoolURL( url ) {
  let formattedURL;
  const protocolRegex = /^https?:\/\//;
  if ( url && protocolRegex.test( url ) ) {
    formattedURL = url;
  } else if ( url ) {
    formattedURL = 'http://' + url;
  } else {
    formattedURL = false;
  }
  return formattedURL;
}

module.exports = formatSchoolURL;
