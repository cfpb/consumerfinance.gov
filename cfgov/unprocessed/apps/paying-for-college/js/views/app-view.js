/* This file handles view items which apply only to the "state" of the
application, and are otherwise inappropriate for the
other views. */
import { buildUrlQueryString } from '../util/url-parameter-utils.js';
import { closest } from '@cfpb/cfpb-atomic-component/src/utilities/dom-traverse.js';
import { recalculateFinancials } from '../dispatchers/update-models.js';
import { sendAnalyticsEvent } from '../util/analytics.js';
import { updateFinancialViewAndFinancialCharts } from '../dispatchers/update-view.js';
import { updateState } from '../dispatchers/update-state.js';
import { getStateValue } from '../dispatchers/get-model-values.js';
const appView = {
  _actionPlanChoices: null,
  _didThisHelpChoices: null,
  _restartBtn: null,
  _saveForLaterBtn: null,
  _saveLinks: null,
  _sendLinkBtn: null,

  /**
   * Handle the click of the Include Parent Plus checkbox
   * @param {Object} event - Click event object
   */
  _handleIncludeParentPlusBtn: event => {
    const target = event.target;
    updateState.byProperty( 'includeParentPlus', target.checked );
    recalculateFinancials();
    updateFinancialViewAndFinancialCharts();
    appView.setUrlQueryString();
  },

  /**
   * Handle clicks of the restart button
   * @param {Object} event - The event object
   */
  _handleRestartBtn: event => {
    event.preventDefault();
    sendAnalyticsEvent( 'button click', 'restart' );
    window.location = '.';
  },

  /**
   * Handle clicks of the 'Save for Later' button
   */
  _handleSaveForLaterBtn: () => {
    sendAnalyticsEvent( 'Save and finish later', window.location.search );
    updateState.byProperty( 'save-for-later', 'active' );
  },

  _handleSendLinkBtn: event => {
    sendAnalyticsEvent( 'Email your link click', window.location.search );

    const target = event.target;
    let href = 'mailto:' + document.querySelector( '#finish_email' ).value;
    href += '?subject=Link: Your financial path to graduation&body=';
    href += encodeURIComponent( window.location.href );
    target.setAttribute( 'href', href );
  },

  /**
   * Update the link on the save and finish page with the current url
   */
  _updateSaveLink: () => {
    appView._saveLinks.forEach( elem => {
      elem.innerText = window.location.href;
    } );
  },

  /**
   * Public method for updating this view
   */
  updateView: () => {
    appView._updateSaveLink();
  },


  updateUI: () => {
    appView._includeParentPlusBtn.checked = getStateValue( 'includeParentPlus' ) ? true : false;
  },
  /**
   * Replaces current state, adding the formatted querystring as the URL
   */
  setUrlQueryString: () => {
    updateState.replaceStateInHistory( buildUrlQueryString() );
    appView._updateSaveLink();
  },

  /**
   * Initialize the View
   */
  init: () => {
    appView._actionPlanChoices = document.querySelectorAll( '.action-plan_choices .m-form-field input.a-radio' );
    appView._didThisHelpChoices = document.querySelectorAll( '[data-impact] .m-form-field input.a-radio' );
    appView._restartBtn = document.querySelector( '[data-app-button="restart"]' );
    appView._saveForLaterBtn = document.querySelector( '[data-app-button="save-and-finish-later"]' );
    appView._saveLinks = document.querySelectorAll( '[data-app-save-link]' );
    appView._sendLinkBtn = document.querySelector( '#email-your-link' );
    appView._includeParentPlusBtn = document.querySelector( '#plan__parentPlusFeeRepay' );

    _addButtonListeners();
  }
};

/**
 * Listeners for buttons.
 */
function _addButtonListeners() {
  appView._didThisHelpChoices.forEach( elem => {
    elem.addEventListener( 'click', _handleDidThisHelpClick );
  } );

  appView._actionPlanChoices.forEach( elem => {
    elem.addEventListener( 'click', _handleActionPlanClick );
  } );

  appView._restartBtn.addEventListener( 'click', appView._handleRestartBtn );
  appView._saveForLaterBtn.addEventListener( 'click', appView._handleSaveForLaterBtn );
  appView._sendLinkBtn.addEventListener( 'click', appView._handleSendLinkBtn );
  appView._includeParentPlusBtn.addEventListener( 'click', appView._handleIncludeParentPlusBtn );
}

/**
 * Handle the click of buttons on final page.
 * @param {MouseEvent} event - Click event object.
 */
function _handleDidThisHelpClick( event ) {
  const button = event.target;
  const parent = closest( button, '.o-form_fieldset' );
  sendAnalyticsEvent( 'Impact question click: ' + parent.dataset.impact, event.target.value );
  updateState.byProperty( parent.dataset.impact, event.target.value );
}

/**
 * Event handling for action-plan choice clicks.
 * @param {MouseEvent} event - Triggering event.
 */
function _handleActionPlanClick( event ) {
  const target = event.target;
  updateState.byProperty( 'actionPlan', target.value );
}

export {
  appView
};
