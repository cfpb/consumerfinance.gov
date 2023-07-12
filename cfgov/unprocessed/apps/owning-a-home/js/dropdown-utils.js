// TODO: Remove jquery.
import $ from 'jquery';

/**
 * Some dropdown utility methods.
 * @param {string|Array} id - ID(s) of the HTML select elements.
 * @returns {object} Methods to manipulate the requested elements.
 */
const utils = function (id) {
  let $el;

  if (!id) {
    throw new Error('You must specify the id of a dropdown.');
  }

  // If they provided an array, select 'em all. Otherwise, just the one.
  $el = id instanceof Array ? $('#' + id.join(', #')) : ($el = $('#' + id));

  /**
   * If optionVal is provided as an array, turn it into a string
   * of attribute selectors. Otherwise, just create a single attribute
   * selector. If no val is provided, return an asterisk to select
   * all elements.
   * @param {string|Array} optionVal - Option(s) in the dropdown to modify.
   * @returns {string} Selector string of values.
   */
  function parseVals(optionVal) {
    let returnVal;

    if (optionVal instanceof Array) {
      returnVal = '[value=' + optionVal.join('],[value=') + ']';
    } else if (optionVal) {
      returnVal = '[value=' + optionVal + ']';
    } else {
      returnVal = '*';
    }

    return returnVal;
  }

  /**
   * Disable a select element's option(s).
   * @param {string|Array} optionVal - The value(s) of the options
   *  that you'd like to disable. Can be a string or an array. If no
   *  option(s) are specified, the entire dropdown is disabled.
   * @returns {object} An instance.
   */
  function disable(optionVal) {
    if (!optionVal) {
      $el.attr('disabled', 'disabled');
    }
    $el
      .find('option')
      .filter(parseVals(optionVal))
      .attr('disabled', 'disabled');

    return this;
  }

  /**
   * Enable a select element's option(s).
   * @param {string|Array} optionVal - The value(s) of the options
   * that you'd like to enable. Can be a string or an array. If no
   * option(s) are specified, the entire dropdown is enabled.
   * @returns {object} An instance.
   */
  function enable(optionVal) {
    if (!optionVal) {
      $el.removeAttr('disabled');
    }
    $el.find('option').filter(parseVals(optionVal)).removeAttr('disabled');

    return this;
  }

  /**
   * @param {object} values - Map of option values.
   * @returns {object} The top-level utils object.
   */
  function addOption(values) {
    const opts = values || {};
    const label = opts.label || '';
    const value = opts.value || '';

    $el.each(function () {
      // If the option already exists, abort.
      if ($el.children("option[value='" + value + "']").length > 0) {
        return;
      }

      const option = document.createElement('option');
      option.value = value;
      option.innerHTML = label;
      $(this).append(option);
    });

    if (opts.select) {
      $el.val(value);
    }

    return this;
  }

  /**
   * Remove an option from a dropdown.
   * @param {string|Array} optionVal - The value(s) of the options
   *  that you'd like to remove. Can be a string or an array. If no
   *  option(s) are specified, all options are removed.
   * @returns {object} The top-level utils object.
   */
  function removeOption(optionVal) {
    if (!optionVal) {
      throw new Error(
        "You must provide the value of the option you'd like to remove.",
      );
    }
    $el.find('option').filter(parseVals(optionVal)).remove();

    return this;
  }

  /**
   * @param {object} value - Map of option values.
   * @returns {object} The top-level utils object.
   */
  function hasOption(value) {
    if (!value) {
      throw new Error(
        "You must provide the value of the option you'd like to check for.",
      );
    }

    return $el.children('option[value=' + value + ']').length > 0;
  }

  /**
   * Resets the select's element to its first option.
   * @returns {object} The top-level utils object.
   */
  function reset() {
    $el.each(function () {
      $(this)[0].selectedIndex = 0;
    });

    return this;
  }

  /**
   * Show a dropdown.
   * @returns {object} The top-level utils object.
   */
  function show() {
    $el.each(function () {
      const $container = $('.' + $(this).attr('id'));
      $container.removeClass('u-hidden');
    });

    return this;
  }

  /**
   * Hide a dropdown.
   * @returns {object} The top-level utils object.
   */
  function hide() {
    $el.each(function () {
      const $container = $('.' + $(this).attr('id'));
      $container.addClass('u-hidden');
    });

    return this;
  }

  /**
   * Show a loading animation.
   * @returns {object} The top-level utils object.
   */
  function showLoading() {
    $el.each(function () {
      const $container = $('.' + $(this).attr('id'));
      $container.addClass('loading');
    });

    return this;
  }

  /**
   * Hide the loading animation.
   * @returns {object} The top-level utils object.
   */
  function hideLoading() {
    $el.each(function () {
      const $container = $('.' + $(this).attr('id'));
      $container.removeClass('loading');
    });

    return this;
  }

  /**
   * Give a dropdown a yellow border to highlight it.
   * @returns {object} The top-level utils object.
   */
  function showHighlight() {
    $el.each(function () {
      $(this).parent().addClass('highlight-dropdown');
    });

    return this;
  }

  /**
   * Remove a dropdown's highlight.
   * @returns {object} The top-level utils object.
   */
  function hideHighlight() {
    $el.each(function () {
      $(this).parent().removeClass('highlight-dropdown');
    });

    return this;
  }

  return {
    disable,
    enable,
    show,
    hide,
    addOption,
    removeOption,
    hasOption,
    showLoadingAnimation: showLoading,
    hideLoadingAnimation: hideLoading,
    showHighlight,
    hideHighlight,
    reset,
  };
};

export default utils;
