import { ajaxRequest as xhr } from '../../../js/modules/util/ajax-request';

const fetch = ( url, cb ) => xhr( 'GET', url, {
  success: data => cb( null, data ),
  fail: err => cb( err )
} );

module.exports = {
  fetch
};
