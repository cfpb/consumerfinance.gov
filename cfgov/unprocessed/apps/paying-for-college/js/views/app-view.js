/* This file handles view items which apply only to the "state" of the
application, and are otherwise inappropriate for the
other views. */

import { bindEvent } from '../../../../js/modules/util/dom-events';
import { closest } from '../../../../js/modules/util/dom-traverse';
import { buildUrlQueryString } from '../util/url-parameter-utils.js';
import { getAllStateValues } from '../dispatchers/get-model-values.js';
import { replaceStateInHistory, updateState } from '../dispatchers/update-state.js';


const appView = {
  _didThisHelpBtns: null,
  _finishLink: '',
  _sendLinkBtn: null,
  _actionPlanChoices: null,

  /**
   * Listeners for buttons
   */
  _addButtonListeners: function() {
    appView._didThisHelpBtns.forEach( elem => {
      bindEvent( elem, { click: this._handleDidThisHelpBtns } );
    } );

    appView._actionPlanChoices.forEach( elem => {
      bindEvent( elem, { click: this._handleActionPlanClick } );
    } );

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
  _handleDidThisHelpBtns: event => {
    const button = event.target;
    const parent = closest( button, '.m-btn-group' );

    // Handle view of the buttons
    // TODO: These are probably better off being radio buttons
    button.classList.remove( 'a-btn__disabled' );
    parent.querySelectorAll( 'button:not( [value="' + button.value + '"]' )
      .forEach( elem => {
        elem.classList.add( 'a-btn__disabled' );
      } );
  },

  _handleSendLinkBtn: event => {
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
    appView._finishLink.innerText = window.location.href;
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
    appView._didThisHelpBtns = document.querySelectorAll( '#save_did-it-help button, #save_understand-loans button' );
    appView._finishLink = document.querySelector( '#finish_link' );
    appView._sendLinkBtn = document.querySelector( '#email-your-link' );
    appView._actionPlanChoices = document.querySelectorAll( '.action-plan_choices .m-form-field input.a-radio' );

    appView._addButtonListeners();
  }
};

export {
  appView
};
