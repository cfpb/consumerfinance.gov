import { analyticsSendEvent } from '@cfpb/cfpb-analytics';
import $ from '../../../../../js/modules/util/dollar-sign.js';

const print = {
  init: function () {
    $('.next-steps__controls > button').on('click', function (evt) {
      evt.preventDefault();
      window.print();
      analyticsSendEvent({ action: 'Step Completed', label: 'Print' });
    });
  },
};

export default print;
