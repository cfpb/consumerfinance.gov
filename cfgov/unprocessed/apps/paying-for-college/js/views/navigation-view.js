// This file contains the 'view' of all financial info, including costs, loans, etc

import { closest } from '../../../../js/modules/util/dom-traverse';
import { updateState } from '../dispatchers/update-state.js';
import { getState } from '../dispatchers/get-state.js';
import { bindEvent } from '../../../../js/modules/util/dom-events';

const navigationView = {
  _navMenu: null,
  _navListItems: null,
  _navButtons: null,
  _nextButtons: null,

  _addButtonListeners: function( ) {
    navigationView._navButtons.forEach( elem => {
      const events = {
        click: this._handleNavButtonClick
      };
      bindEvent( elem, events );
    } );

    navigationView._nextButtons.forEach( elem => {
      const events = {
        click: this._handleNextButtonClick
      };
      bindEvent( elem, events );
    } );
  },

  _handleNavButtonClick: function( event ) {
    const target = event.target;
    if ( typeof target.dataset.nav_item !== 'undefined' ) {
      updateState.activeSection( target.dataset.nav_item );
    } else if ( typeof target.dataset.nav_section !== 'undefined' ) {
      const parent = closest( target, '.o-college-costs-nav__section' );
      const elem = parent.querySelector( '.o-college-costs-nav__section ul li button' );
      updateState.activeSection( elem.dataset.nav_item );
    }
  },

  _handleNextButtonClick: function( event ) {
    const target = event.target;
    console.log( event.target.dataset );
    updateState.activeSection( event.target.dataset.buttonTarget );
    // The user should be sent back to the top of the P4C content
    window.scrollTo( 0, document.querySelector( '.college-costs' ).offsetTop );

  },

  _updateActiveSection: function() {
    const activeName = getState( 'activeSection' );
    const activeElem = closest( this._navMenu.querySelector( '[data-nav_item="' + activeName + '"]' ), 'li' );
    const activeParent = closest( activeElem, '.o-college-costs-nav__section' );
    this._navListItems.forEach( elem => {
      elem.classList.remove( 'active' );
    } );

    activeElem.classList.add( 'active' );
    activeParent.classList.add( 'active' );
  },

  init: function( body ) {
    this._navMenu = body.querySelector( '.o-college-costs-nav' );
    this._navButtons = body.querySelectorAll( '.o-college-costs-nav button' );
    this._navListItems = body.querySelectorAll( '.o-college-costs-nav li' );
    this._nextButtons = body.querySelectorAll( '.college-costs_tool-section .btn__next-step' );

    this._addButtonListeners();

  },

  update: function() {
    this._updateActiveSection();
  }

};

export {
  navigationView
};
