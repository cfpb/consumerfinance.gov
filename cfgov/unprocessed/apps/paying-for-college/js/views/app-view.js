/* This file handles view items which apply only to the "state" of the
application, and are otherwise inappropriate for the
other views. */

import { replaceStateInHistory, updateState } from '../dispatchers/update-state.js';
import { bindEvent } from '../../../../js/modules/util/dom-events';
import { buildUrlQueryString } from '../util/url-parameter-utils.js';
import { closest } from '../../../../js/modules/util/dom-traverse';
import { getAllStateValues } from '../dispatchers/get-model-values.js';
import { sendAnalyticsEvent } from '../util/analytics.js';


const appView = {
  _actionPlanChoices: null,
  _didThisHelpChoices: null,
  _restartBtn: null,
  _saveForLaterBtn: null,
  _saveLinks: null,
  _sendLinkBtn: null,

  /**
   * Listeners for buttons
   */
  _addButtonListeners: function() {
    appView._didThisHelpChoices.forEach( elem => {
      bindEvent( elem, { click: this._handleDidThisHelpClick } );
    } );

    appView._actionPlanChoices.forEach( elem => {
      bindEvent( elem, { click: this._handleActionPlanClick } );
    } );

    bindEvent( appView._restartBtn, { click: appView._handleRestartBtn } );
    bindEvent( appView._saveForLaterBtn, { click: appView._handleSaveForLaterBtn } );
    bindEvent( appView._sendLinkBtn, { click: appView._handleSendLinkBtn } );
  },

  /**
   * Event handling for action-plan choice clicks
   * @param {Object} event - Triggering event
   */
  _handleActionPlanClick: function( event ) {
    const target = event.target;
    updateState.byProperty( 'actionPlan', target.value );
  },

  /**
   * Handle the click of buttons on final page
   * @param {Object} event - Click event object
   */
  _handleDidThisHelpClick: event => {
    const button = event.target;
    const parent = closest( button, '.o-form_fieldset' );
    sendAnalyticsEvent( 'Impact question click: ' + parent.dataset.impact, event.target.value );
    updateState.byProperty( parent.dataset.impact, event.target.value );
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
    href += window.location.href;
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

    appView._addButtonListeners();
  }
};

export {
  appView
};
