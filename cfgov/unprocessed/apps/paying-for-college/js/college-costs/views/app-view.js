/* This file handles view items which apply only to the "state" of the
application, and are otherwise inappropriate for the
other views. */
import { buildUrlQueryString } from '../util/url-parameter-utils.js';
import { recalculateFinancials } from '../dispatchers/update-models.js';
import { sendAnalyticsEvent } from '../util/analytics.js';
import { updateFinancialViewAndFinancialCharts } from '../dispatchers/update-view.js';
import { updateState } from '../dispatchers/update-state.js';
import { CostsGroup } from '../CostsGroup.js';

const HIDDEN_CLASS = 'u-hidden';
const appView = {
  _actionPlanChoices: null,
  _didThisHelpChoices: null,
  _restartBtn: null,
  _saveForLaterBtn: null,
  _saveLinks: null,
  _sendLinkBtn: null,
  _copyLinkBtn: null,
  _copyBtnDefaultText: null,
  _copyBtnSuccessText: null,

  /**
   * Handle the click of the Include Parent Plus checkbox
   * @param {object} event - Click event object
   */
  _handleIncludeParentPlusBtn: (event) => {
    const target = event.target;
    updateState.byProperty('includeParentPlus', target.checked);
    recalculateFinancials();
    updateFinancialViewAndFinancialCharts();
    appView.setUrlQueryString();
  },

  /**
   * Handle clicks of the restart button
   * @param {object} event - The event object
   */
  _handleRestartBtn: (event) => {
    event.preventDefault();
    sendAnalyticsEvent('button click', 'restart');
    window.location = '.';
  },

  /**
   * Handle clicks of the 'Save for Later' button
   */
  _handleSaveForLaterBtn: () => {
    sendAnalyticsEvent('Save and finish later', window.location.search);
    updateState.byProperty('save-for-later', 'active');
  },

  _handleCopyLinkBtn: (event) => {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(window.location.href).then(function () {
        const btn = event.target.closest('button');
        const copyBtnDefaultText = btn.querySelector('#default-text');
        const copyBtnSuccessText = btn.querySelector('#success-text');
        copyBtnDefaultText.classList.add(HIDDEN_CLASS);
        copyBtnSuccessText.classList.remove(HIDDEN_CLASS);
        setTimeout(function () {
          copyBtnSuccessText.classList.add(HIDDEN_CLASS);
          copyBtnDefaultText.classList.remove(HIDDEN_CLASS);
        }, 3000);
      });
    } else if (window.clipboardData && window.clipboardData.setData) {
      window.clipboardData.setData('Text', window.location.href);
    }
  },

  _handleCopyLinkBtnKeypress: (event) => {
    if (event.key === 'Enter') {
      appView._handleCopyLinkBtn(event);
    }
  },

  /**
   * Update the link on the save and finish page with the current url
   */
  _updateSaveLink: () => {
    appView._saveLinks.forEach((elem) => {
      elem.innerText = window.location.href;
    });
  },

  /**
   * Public method for updating this view
   */
  updateView: () => {
    appView._updateSaveLink();
  },

  updateUI: () => {},

  /**
   * Replaces current state, adding the formatted querystring as the URL
   */
  setUrlQueryString: () => {
    updateState.replaceStateInHistory(buildUrlQueryString());
    appView._updateSaveLink();
  },

  /**
   * Initialize the View
   */
  init: () => {
    appView._actionPlanChoices = document.querySelectorAll(
      '.action-plan__choices .m-form-field input.a-radio',
    );
    appView._didThisHelpChoices = document.querySelectorAll(
      '[data-impact] .m-form-field input.a-radio',
    );
    appView._restartBtn = document.querySelector('[data-app-button="restart"]');
    appView._saveForLaterBtn = document.querySelector(
      '.a-btn--link[data-destination="save-finish"]',
    );
    appView._saveLinks = document.querySelectorAll('[data-app-save-link]');
    appView._copyLinkBtn = document.querySelectorAll('.copy-your-link');
    appView._includeParentPlusBtn = document.querySelector(
      '#plan__parentPlusFeeRepay',
    );

    _addButtonListeners();
  },
};

/**
 * Listeners for buttons.
 */
function _addButtonListeners() {
  appView._didThisHelpChoices.forEach((elem) => {
    elem.addEventListener('click', _handleDidThisHelpClick);
  });

  appView._actionPlanChoices.forEach((elem) => {
    elem.addEventListener('click', _handleActionPlanClick);
    elem.addEventListener('focus', _handleActionPlanClick);
  });

  appView._restartBtn.addEventListener('click', appView._handleRestartBtn);
  appView._saveForLaterBtn.addEventListener(
    'click',
    appView._handleSaveForLaterBtn,
  );
  appView._copyLinkBtn.forEach((elem) => {
    elem.addEventListener('click', appView._handleCopyLinkBtn);
    elem.addEventListener('keyup', appView._handleCopyLinkBtnKeypress);
  });
}

/**
 * Handle the click of buttons on final page.
 * @param {MouseEvent} event - Click event object.
 */
function _handleDidThisHelpClick(event) {
  const parent = event.target.closest('.o-form__fieldset');
  sendAnalyticsEvent(
    'Impact question click: ' + parent.dataset.impact,
    event.target.value,
  );
  updateState.byProperty(parent.dataset.impact, event.target.value);
}

/**
 * Event handling for action-plan choice clicks.
 * @param {MouseEvent} event - Triggering event.
 */
function _handleActionPlanClick(event) {
  const target = event.target;
  target.setAttribute('checked', 'checked');
  updateState.byProperty('actionPlan', target.value);
}

/**
 * Initialize Costs Groups organism
 */
const collegeCosts = document.querySelector('.college-costs');
CostsGroup.init(collegeCosts);

export { appView };
