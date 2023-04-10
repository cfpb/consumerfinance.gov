import { analyticsSendEvent } from '@cfpb/cfpb-analytics';
import { Delay, addEventListenerToElem } from './util/analytics-util';

(function () {
  // credit score slider
  const rangeSliders = document.querySelectorAll('.rangeslider');
  let rangeSliderEl;
  for (let i = 0, len = rangeSliders.length; i < len; i++) {
    rangeSliderEl = rangeSliders[i];
    addEventListenerToElem(rangeSliderEl, 'click', _rangeSliderEventHandler);
    addEventListenerToElem(rangeSliderEl, 'touchend', _rangeSliderEventHandler);
  }

  /**
   * Event handler for range slider interactions.
   */
  function _rangeSliderEventHandler() {
    const sliderRangeEl = document.querySelector('#slider-range');
    const score = sliderRangeEl.textContent;
    analyticsSendEvent({
      event: 'OAH Rate Tool Interactions',
      action: 'Score range',
      label: score,
    });
  }

  // state select
  const locationEl = document.querySelector('#location');
  addEventListenerToElem(locationEl, 'change', function (evt) {
    const target = evt.target;
    const value = target.value;
    analyticsSendEvent({
      event: 'OAH Rate Tool Interactions',
      action: 'Select state',
      label: value,
    });
  });

  // house price
  const housePriceDelay = new Delay();
  const housePriceEl = document.querySelector('#house-price');
  addEventListenerToElem(housePriceEl, 'keyup', function (evt) {
    const target = evt.target;
    const value = target.value;
    housePriceDelay(() => {
      analyticsSendEvent({
        event: 'OAH Rate Tool Interactions',
        action: 'House price',
        label: value,
      });
    }, 5000);
  });

  // down payment percentage
  const percentDownDelay = new Delay();
  const percentDownEl = document.querySelector('#percent-down');
  addEventListenerToElem(percentDownEl, 'keyup', function (evt) {
    const target = evt.target;
    const value = target.value;
    percentDownDelay(() => {
      analyticsSendEvent({
        event: 'OAH Rate Tool Interactions',
        action: 'Down payment percent',
        label: value,
      });
    }, 5000);
  });

  // down payment $
  const downPaymentDelay = new Delay();
  const downPaymentEl = document.querySelector('#down-payment');
  addEventListenerToElem(downPaymentEl, 'keyup', function (evt) {
    const target = evt.target;
    const value = target.value;
    downPaymentDelay(() => {
      analyticsSendEvent({
        event: 'OAH Rate Tool Interactions',
        action: 'Down payment amount',
        label: value,
      });
    }, 5000);
  });

  // rate structure
  const rateStructureEl = document.querySelector('#rate-structure');
  addEventListenerToElem(rateStructureEl, 'change', function (evt) {
    const target = evt.target;
    const value = target.value;
    analyticsSendEvent({
      event: 'OAH Rate Tool Interactions',
      action: 'Rate structure',
      label: value,
    });
  });

  // loan term
  const loanTermEl = document.querySelector('#loan-term');
  addEventListenerToElem(loanTermEl, 'change', function (evt) {
    const target = evt.target;
    const value = target.value;
    analyticsSendEvent({
      event: 'OAH Rate Tool Interactions',
      action: 'Loan term',
      label: value,
    });
  });

  // loan type
  const loanTypeEl = document.querySelector('#loan-type');
  addEventListenerToElem(loanTypeEl, 'change', function (evt) {
    const target = evt.target;
    const value = target.value;
    analyticsSendEvent({
      event: 'OAH Rate Tool Interactions',
      action: 'Loan type',
      label: value,
    });
  });

  // arm type
  const armTypeEl = document.querySelector('#arm-type');
  addEventListenerToElem(armTypeEl, 'change', function (evt) {
    const target = evt.target;
    const value = target.value;
    analyticsSendEvent({
      event: 'OAH Rate Tool Interactions',
      action: 'ARM type',
      label: value,
    });
  });

  // rate comparison select #1
  const rateCompare1El = document.querySelector('#rate-compare-1');
  addEventListenerToElem(rateCompare1El, 'change', function (evt) {
    const target = evt.target;
    const value = target.value;
    analyticsSendEvent({
      event: 'OAH Rate Tool Interactions',
      action: 'Interest cost 1',
      label: value,
    });
  });

  // rate comparison select #2
  const rateCompare2El = document.querySelector('#rate-compare-2');
  addEventListenerToElem(rateCompare2El, 'change', function (evt) {
    const target = evt.target;
    const value = target.value;
    analyticsSendEvent({
      event: 'OAH Rate Tool Interactions',
      action: 'Interest cost 2',
      label: value,
    });
  });

  // page reload link
  const reloadLinkEl = document.querySelector('#reload-link');
  addEventListenerToElem(reloadLinkEl, 'click', function () {
    analyticsSendEvent({
      event: 'OAH Rate Tool Interactions',
      action: 'Revert',
      label: '/owning-a-home/rate-checker',
    });
  });

  // next steps: I plan to buy in the next couple of months
  const planToBuyTabEl = document.querySelector('#plan-to-buy-tab');
  addEventListenerToElem(planToBuyTabEl, 'click', function () {
    analyticsSendEvent({
      event: 'OAH Rate Tool Interactions',
      action: 'Click',
      label: 'Collapsed_Tabs_Buying',
    });
  });

  // next steps: I won't buy for several months
  const wontBuyTabEl = document.querySelector('#wont-buy-tab');
  addEventListenerToElem(wontBuyTabEl, 'click', function () {
    analyticsSendEvent({
      event: 'OAH Rate Tool Interactions',
      action: 'Click',
      label: 'Collapsed_Tabs_Not_Buying',
    });
  });
})();
