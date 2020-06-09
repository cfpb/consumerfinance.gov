// This file contains the 'view' of all financial info, including costs, loans, etc

import { closest } from '../../../../js/modules/util/dom-traverse';
import { updateState } from '../dispatchers/update-state.js';
import { bindEvent } from '../../../../js/modules/util/dom-events';
import { getStateValue } from '../dispatchers/get-model-values.js';

const navigationView = {
  _contentSidebar: null,
  _introduction: null,
  _sections: null,
  _navMenu: null,
  _navListItems: null,
  _navButtons: null,
  _nextButton: null,
  _appSegment: null,

  _addButtonListeners: function( ) {
    navigationView._navButtons.forEach( elem => {
      const events = {
        click: this._handleNavButtonClick
      };
      bindEvent( elem, events );
    } );

    bindEvent( navigationView._nextButton, { click: this._handleNextButtonClick } );

    bindEvent( navigationView._getStartedBtn, { click: this._handleGetStartedBtnClick } );
  },

  _handleGetStartedBtnClick: function( event ) {
    updateState.getStarted( true );
    updateState.activeSection( 'school-info' );
    navigationView.updateView();

    // The user should be sent back to the top of the P4C content
    window.scrollTo( 0, document.querySelector( '.college-costs' ).offsetTop );
  },

  _handleNavButtonClick: function( event ) {
    event.preventDefault();
    const target = event.target;

    // Click on a nav menu page link
    if ( typeof target.dataset.nav_item !== 'undefined' ) {
      updateState.activeSection( target.dataset.nav_item );

    // Click on a nav section header
    } else if ( typeof target.dataset.nav_section !== 'undefined' ) {
      // Close all open menu section
      navigationView._navListItems.forEach( elem => {
        elem.setAttribute( 'data-nav-is-active', 'False' );
        elem.setAttribute( 'data-nav-is-open', 'False' );
      } );
      // Open the clicked menu section
      closest( target, 'li' ).setAttribute( 'data-nav-is-open', 'True' );
    }
  },

  _handleNextButtonClick: function( event ) {
    updateState.nextSection();
    window.scrollTo( 0, document.querySelector( '.college-costs' ).offsetTop );
  },

  _updateSideNav: function( activeName ) {
    const navItem = navigationView._navMenu.querySelector( '[data-nav_item="' + activeName + '"]' );
    const activeElem = closest( navItem, 'li' );
    const activeParent = closest( activeElem, 'li' );

    this._navListItems.forEach( elem => {
      elem.setAttribute( 'data-nav-is-active', 'False' );
      elem.setAttribute( 'data-nav-is-open', 'False' );
    } );

    activeElem.setAttribute( 'data-nav-is-active', 'True' );
    activeParent.setAttribute( 'data-nav-is-open', 'True' );
    activeParent.setAttribute( 'data-nav-is-active', 'True' );

  },

  _showAndHideSections: function( activeName ) {
    const query = '.college-costs_tool-section[data-tool-section="' + activeName + '"]';
    const activeSection = document.querySelector( query );

    this._sections.forEach( elem => {
      elem.classList.remove( 'active' );
    } );

    activeSection.classList.add( 'active' );
  },

  updateView: function() {
    const started = getStateValue( 'gotStarted' );
    if ( started ) {
      const activeName = getStateValue( 'activeSection' );
      this._updateSideNav( activeName );
      this._showAndHideSections( activeName );
    }
  },

  init: function( body ) {
    this._navMenu = body.querySelector( '.o-secondary-navigation' );
    this._navButtons = body.querySelectorAll( '.o-secondary-navigation a' );
    this._navListItems = body.querySelectorAll( '.o-secondary-navigation li' );
    this._nextButton = body.querySelector( '.college-costs_tool-section_buttons .btn__next-step' );
    this._contentSidebar = body.querySelector( '.content_sidebar' );
    this._introduction = body.querySelector( '.college-costs_intro-segment' );
    this._getStartedBtn = body.querySelector( '.college-costs_intro-segment .btn__get-started' );
    this._appSegment = body.querySelector( '.college-costs_app-segment' );
    this._sections = body.querySelectorAll( '.college-costs_tool-section' );

    this._addButtonListeners();

    this.updateView();

  }

};

export {
  navigationView
};
