import $ from '../../../../../js/modules/util/dollar-sign.js';
import { analyticsSendEvent } from '@cfpb/cfpb-analytics';
import getExpenses from '../dispatchers/get-expenses-values.js';
import publish from '../dispatchers/publish-update.js';
import {
  convertStringToNumber,
  formatUSD,
} from '../../../../../js/modules/util/format.js';

const expensesView = {
  $elements: $('[data-expenses]'),
  $reviewAndEvaluate: $('[data-section="review"], [data-section="evaluate"]'),
  currentInput: '',

  init: function () {
    this.expenseInputChangeListener();
    this.keyupListener();
    this.regionSelectListener();
  },

  /**
   * Helper function that updates the value or text of an element
   * @param {object} $ele - jQuery object of the element to update
   * @param {number|string} value - The new value
   * @param {boolean} currency - True if value is to be formatted as currency
   */
  updateElement: function ($ele, value, currency) {
    const originalValue = $ele.val() || $ele.text();
    const isSummaryLineItem = $ele.attr('data-line-item') === 'true';
    if (currency === true) {
      value = formatUSD({ amount: value, decimalPlaces: 0 });
    }
    if ($ele.tagName() === 'INPUT') {
      $ele.val(value);
    } else if (isSummaryLineItem && originalValue !== value) {
      setTimeout(function () {
        expensesView.removeRecalculationMessage($ele, value);
      }, 2000);
      expensesView.addSummaryRecalculationMessage($ele);
    } else {
      $ele.text(value);
    }
  },

  /**
   * Helper function that updates expenses elements
   * @param {object} values - expenses model values
   */
  updateExpenses: function (values) {
    const expensesHigherThanSalary = $('.aid-form__higher-expenses');
    this.$elements.each((elem) => {
      const $ele = $(elem);
      const name = $ele.attr('data-expenses');
      const currency = true;
      if (expensesView.currentInput !== $ele.attr('id')) {
        expensesView.updateElement($ele, values[name], currency);
      }
      if (values.monthlyLeftover > 0) {
        expensesHigherThanSalary.hide();
        analyticsSendEvent({
          action: 'Total left at the end of the month',
          label: 'Zero left to pay',
        });
      } else {
        expensesHigherThanSalary.show();
      }
    });
  },

  /**
   * Function that updates the view with new values
   * @param {object} values - expense model values
   */
  updateView: function (values) {
    // handle non-private-loan fields
    this.updateExpenses(values);
  },

  /**
   * Helper function for handling user entries in expenses model INPUT fields.
   * @param {string} id - The id attribute of the element to be handled.
   */
  inputHandler: function (id) {
    const ele = document.querySelector('#' + id);
    const value = convertStringToNumber(ele.value);
    const key = ele.getAttribute('data-expenses');
    publish.expensesData(key, value);
    expensesView.updateView(getExpenses.values());
  },

  /**
   * Helper function to indicate that a offer summary line item has
   * successfully recalculated
   * @param {object} element - jQuery object of the recalculated summary element
   */
  addSummaryRecalculationMessage: function (element) {
    element.siblings().hide();
    element.text('Updating...');
  },

  /**
   * Helper function to remove all indicators that data has recalculated
   * @param {object} element - jQuery object of the recalculated summary element
   * @param {string} value - the recalculated value of the element
   */
  removeRecalculationMessage: function (element, value) {
    element.text(value);
    element.siblings().show();
  },

  /**
   * Listener function for keyup in expenses INPUT fields
   */
  keyupListener: function () {
    this.$reviewAndEvaluate.each(() => {
      $('[data-expenses]').each((elmo) => {
        elmo.addEventListener('keyup focusout', function () {
          clearTimeout(expensesView.keyupDelay);
          expensesView.currentInput = $(this).attr('id');
          if ($(this).is(':focus')) {
            expensesView.keyupDelay = setTimeout(function () {
              expensesView.inputHandler(expensesView.currentInput);
              expensesView.updateView(getExpenses.values());
            }, 500);
          } else {
            expensesView.inputHandler(expensesView.currentInput);
            expensesView.currentInput = 'none';
            expensesView.updateView(getExpenses.values());
          }
        });
      });
    });
  },

  /**
   * Listener function for change events on expenses INPUT fields
   */
  expenseInputChangeListener: function () {
    $('[data-expenses]').each((elmo) => {
      elmo.addEventListener('change', function () {
        const expenses = $(this).data('expenses');
        if (expenses) {
          analyticsSendEvent({ action: 'Value Edited', label: expenses });
        }
      });
    });
  },

  /**
   * Listener for the BLS region SELECT
   */
  regionSelectListener: function () {
    $('#bls-region-select').listen('change', function (event) {
      const region = event.target.value || 'NE';
      publish.updateRegion(region);
      expensesView.updateView(getExpenses.values());
      analyticsSendEvent({ action: 'Region Changed', label: region });
    });
  },
};

export default expensesView;
