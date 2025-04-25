import jsonpPModule from 'jsonp-p';
const jsonpP = jsonpPModule.default;
import { addEl, createEl, removeClass } from './dom-tools.js';
import { incrementTotal } from './count.js';

/**
 * Call the census.gov API and display an error if warranted.
 * @param {string} address - An address.
 * @param {Array} ruralCounties - Rural counties for a chosen year.
 * @param {Function} cb - Callback to call.
 */
function callCensus(address, ruralCounties, cb) {
  const url =
    'https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?' +
    'address=' +
    address +
    '&benchmark=4' +
    '&format=jsonp';

  jsonpP(url)
    .promise.then(function (data) {
      cb(data, ruralCounties);
    })
    .catch(function (error) {
      if (error) {
        const addressElement = createEl(`<li>${address}</li>`);

        addEl(document.querySelector('#process-error-desc'), addressElement);
        removeClass('#process-error', 'u-hidden');

        incrementTotal();
      }
    });
}

export default callCensus;
