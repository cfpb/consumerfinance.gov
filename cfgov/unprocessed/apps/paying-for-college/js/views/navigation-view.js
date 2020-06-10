// This file contains the 'view' of all financial info, including costs, loans, etc

import { closest } from '../../../../js/modules/util/dom-traverse';
import { updateState } from '../dispatchers/update-state.js';
import { bindEvent } from '../../../../js/modules/util/dom-events';
import { getStateValue, getAllStateValues } from '../dispatchers/get-model-values.js';

const navigationView = {
  _contentSidebar: null,
  _introduction: null,
  _sections: null,
  _navMenu: null,
  _navListItems: null,
  _navButtons: null,
  _nextButton: null,
  _appSegment: null,
  _stateDomElememnt: null,

  /**
   * _addButtonListeners - Add event listeners for nav buttons
   */
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

  /**
   * _addPopStateListener - Add a listener for "popstate" events
   */
  _addPopStateListener: function() {
    const events = {
      popstate: navigationView._handlePopState
    };
    bindEvent( window, events );
  },

  /**
   * _handleGetStartedBtnClick - Handle the click of the "Get Started" button
   * @param {Object} event - the click event
   */
  _handleGetStartedBtnClick: function( event ) {
    updateState.getStarted( true );
    updateState.activeSection( 'school-info' );
    navigationView.updateView();

    // The user should be sent back to the top of the P4C content
    window.scrollTo( 0, document.querySelector( '.college-costs' ).offsetTop );
  },

  /**
   * _handlePopState - handle popstate events
   * @param {Object} event - the popstate event
   */
  _handlePopState: function( event ) {
    if ( event.state ) {
      window.history.replaceState( getAllStateValues(), null, '' );

      updateState.activeSection( event.state.activeSection );
    }

    updateNavigationView();

  },

  /**
   * _handleNavButtonClick - Handle click event for secondary nav
   * @param {Object} event - click event
   */
  _handleNavButtonClick: function( event ) {
    event.preventDefault();
    const target = event.target;
    if ( typeof target.dataset.nav_item !== 'undefined' ) {
      updateState.activeSection( target.dataset.nav_item );
    } else if ( typeof target.dataset.nav_section !== 'undefined' ) {
      // Close all open menu section
      navigationView._navMenu.querySelectorAll('[data-nav-is-open="True"]').forEach( elem => {
        elem.setAttribute('data-nav-is-open', 'False');
      } );

      // Open the clicked menu section
      const parent = closest( target, '.m-list_item__parent' );
      parent.setAttribute('data-nav-is-open', 'True');

      /* const elem = parent.querySelector( '.o-college-costs-nav__section ul li button' );
         updateState.activeSection( elem.dataset.nav_item ); */
    }
  },

  /**
   * _handleNextButtonClick - handle the click event for the "Next" button
   * @param {Object} event - click event
   */
  _handleNextButtonClick: function( event ) {
    updateState.nextSection();
    window.scrollTo( 0, document.querySelector( '.college-costs' ).offsetTop );
  },

  /**
   * _updateSideNav - Update the side nav
   * @param {String} activeName - name of the active app section
   */
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

  /**
   * _showAndHideSections - Hide all app sections, then show appropriate ones
   * @param {String} activeName - Name of the active section
   */
  _showAndHideSections: function( activeName ) {
    const query = '.college-costs_tool-section[data-tool-section="' + activeName + '"]';
    const activeSection = document.querySelector( query );

    this._sections.forEach( elem => {
      elem.classList.remove( 'active' );
    } );

    activeSection.classList.add( 'active' );
  },

  /**
   * updateView - Public method to run private update methods
   */
  updateView: function() {
    const started = getStateValue( 'gotStarted' );
    if ( started ) {
      const activeName = getStateValue( 'activeSection' );
      this._updateSideNav( activeName );
      this._showAndHideSections( activeName );
    }
  },

  /**
   * updateStateInDom - manages dataset for the MAIN element, which helps display UI elements
   * properly
   * @param {String} property - The state property to modify
   * @param {String} value - The new value of the property
   * NOTE: if the value is null or the Boolean 'false', the data attribute will be removed
   */
  updateStateInDom: function( property, value ) {
    if ( value === false || value === null ) {
      navigationView._stateDomElem.removeAttribute( property );
    } else {
      navigationView._stateDomElem.setAttribute( 'data-state_' + property, value );
    }
  },

  /**
   * init - Initialize the navigation view
   * @param { Object } body - The body element of the page
   */
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

    window.history.replaceState( getAllStateValues(), null, '' );
    this._stateDomElem = document.querySelector( 'main.college-costs' );
    this._addPopStateListener();


  }

};

export {
  navigationView
};
