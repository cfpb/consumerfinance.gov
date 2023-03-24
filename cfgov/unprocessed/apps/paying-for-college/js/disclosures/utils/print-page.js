// TODO: Remove jquery.
import $ from 'jquery';

import { analyticsSendEvent } from '@cfpb/cfpb-analytics';

$(document).ready(function () {
  $('.next-steps_controls > button').on('click', function (evt) {
    evt.preventDefault();
    window.print();
    analyticsSendEvent({ action: 'Step Completed', label: 'Print' });
  });
});
