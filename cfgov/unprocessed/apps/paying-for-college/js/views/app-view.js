/* This file handles view items which apply only to the "state" of the
application, and are otherwise inappropriate for the
other views. */

import { bindEvent } from '../../../../js/modules/util/dom-events';
import { closest } from '../../../../js/modules/util/dom-traverse';
import { buildUrlQueryString } from '../util/url-parameter-utils.js';
import { getAllStateValues } from '../dispatchers/get-model-values.js';


const appView = {
  _didThisHelpBtns: null,
  _finishLink: '',
  _sendLinkBtn: null,

  /**
   * Listeners for buttons
   */
  _addButtonListeners: function() {
    appView._didThisHelpBtns.forEach( elem => {
      const events = {
        click: this._handleDidThisHelpBtns
      };
      bindEvent( elem, events );
    } );

    bindEvent( appView._sendLinkBtn, { click: appView._handleSendLinkBtn } );
  },

  /**
   * Handle the click of buttons on final page
   * @param {Object} event - Click event object
   */
  _handleDidThisHelpBtns: event => {
    const button = event.target;
    const parent = closest( button, '.m-btn-group' );
    button.classList.remove( 'a-btn__disabled');
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
    window.history.replaceState( getAllStateValues(), null, buildUrlQueryString() );
    appView._updateSaveLink();
  },

  /**
   * Initialize the View
   */
  init: () => {
    appView._didThisHelpBtns = document.querySelectorAll( '#save_did-it-help button, #save_understand-loans button' );
    appView._finishLink = document.querySelector( '#finish_link' );
    appView._sendLinkBtn = document.querySelector( '#email-your-link' );

    appView._addButtonListeners();
  }
};

export {
  appView
};
