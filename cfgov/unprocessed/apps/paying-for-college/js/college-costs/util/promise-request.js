/* Promise requests are better. */

/**
 * promiseRequest - A handy function for returning XHR Promises
 * @param {string} method - The method, ex. POST or GET
 * @param {string} url - The url to be requested
 * @returns {object} Promise of the XHR request
 */
function promiseRequest(method, url) {
  const xhr = new XMLHttpRequest();

  return new Promise(function (resolve, reject) {
    // Completed xhr
    xhr.onreadystatechange = function () {
      // Do not run unless xhr is complete
      if (xhr.readyState !== 4) return;
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(xhr);
      } else {
        reject(new Error(xhr.status + ', ' + xhr.statusText));
      }
    };

    xhr.open(method, url, true);

    xhr.send();
  });
}

export { promiseRequest };
