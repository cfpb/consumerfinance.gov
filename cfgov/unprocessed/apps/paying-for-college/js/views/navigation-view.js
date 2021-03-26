// This file contains the 'view' of all financial info, including costs, loans, etc

import {
  getAllStateValues,
  getStateValue
} from '../dispatchers/get-model-values.js';
import { closest } from '@cfpb/cfpb-atomic-component/src/utilities/dom-traverse.js';
import { sendAnalyticsEvent } from '../util/analytics.js';
import { updateState } from '../dispatchers/update-state.js';

const navigationView = {
  _contentSidebar: null,
  _introduction: null,
  _sections: null,
  _navMenu: null,
  _navListItems: null,
  _navItems: null,
  _navButtons: null,
  _nextButton: null,
  _appSegment: null,
  _stateDomElem: null,
  _affordingChoices: null,

  /**
   * _handlePopState - handle popstate events
   * @param {Object} event - the popstate event
   */
  _handlePopState: function( event ) {
    if ( event.state ) {
      const values = getAllStateValues();
      values.activeSection = event.state.activeSection;
      updateState.replaceStateInHistory( window.location.search );
      updateState.activeSection( values.activeSection, true );
    }
  },

  /**
   * _updateSideNav - Update the side nav
   * @param {String} activeName - name of the active app section
   */
  _updateSideNav: function( activeName ) {
    if ( typeof activeName === 'undefined' ) {
      activeName = getStateValue( 'activeSection' );
    }
    // clear active-sections
    navigationView._navItems.forEach( elem => {
      elem.classList.remove( 'active-section' );
      elem.setAttribute( 'aria-selected', false );
    } );

    const navItem = document.querySelector( '[data-nav_item="' + activeName + '"]' );
    const activeElem = closest( navItem, 'li' );
    const activeParent = closest( activeElem, '.m-list_item__parent' );

    this._navListItems.forEach( elem => {
      elem.setAttribute( 'data-nav-is-active', 'False' );
      elem.setAttribute( 'data-nav-is-open', 'False' );
    } );

    activeElem.setAttribute( 'data-nav-is-active', 'True' );
    activeElem.setAttribute( 'aria-selected', true );
    activeParent.setAttribute( 'data-nav-is-open', 'True' );
    activeParent.setAttribute( 'data-nav-is-active', 'True' );
    activeElem.setAttribute( 'aria-selected', true );
    activeParent.querySelectorAll( '.m-list_item' ).forEach( elem => {
      elem.setAttribute( 'data-nav-is-active', 'True' );
    } );

    navItem.classList.add( 'active-section' );
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
    const activeName = getStateValue( 'activeSection' );
    if ( started && activeName ) {
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
      navigationView._stateDomElem.removeAttribute( 'data-state_' + property );
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
    this._navItems = body.querySelectorAll( '[data-nav_item]' );
    this._nextButton = body.querySelector( '.college-costs_tool-section_buttons .btn__next-step' );
    this._contentSidebar = body.querySelector( '.content_sidebar' );
    this._introduction = body.querySelector( '.college-costs_intro-segment' );
    this._getStartedBtn = body.querySelector( '.college-costs_intro-segment .btn__get-started' );
    this._appSegment = body.querySelector( '.college-costs_app-segment' );
    this._sections = body.querySelectorAll( '.college-costs_tool-section' );
    this._stateDomElem = document.querySelector( 'main.college-costs' );
    this._affordingChoices = document.querySelectorAll( '.affording-loans-choices .m-form-field' );

    _addButtonListeners();
    this.updateView();

    updateState.replaceStateInHistory( window.location.search );
    window.addEventListener( 'popstate', navigationView._handlePopState );
  }
};

/**
 * _addButtonListeners - Add event listeners for nav buttons
 */
function _addButtonListeners() {
  navigationView._navButtons.forEach( elem => {
    elem.addEventListener( 'click', _handleNavButtonClick );
  } );

  navigationView._affordingChoices.forEach( elem => {
    elem.addEventListener( 'click', _handleAffordingChoicesClick );
  } );

  navigationView._nextButton.addEventListener( 'click', _handleNextButtonClick );
  navigationView._getStartedBtn.addEventListener( 'click', _handleGetStartedBtnClick );
}

/**
 * _handleAffordingChoicesClick - Handle clicks on Affording Payment choices.
 * @param {MouseEvent} event - The click event object.
 */
function _handleAffordingChoicesClick( event ) {
  const parent = closest( event.target, '.m-form-field' );
  const input = parent.querySelector( 'input[name="affording-display-radio"]' );
  updateState.byProperty( 'expensesChoice', input.value );
}

/**
 * _handleGetStartedBtnClick - Handle the click of the "Get Started" button.
 * @param {MouseEvent} event - the click event object.
 */
function _handleGetStartedBtnClick( event ) {
  updateState.getStarted( true );
  updateState.activeSection( 'school-info' );
  navigationView.updateView();

  // The user should be sent back to the top of the P4C content
  window.scrollTo( 0, document.querySelector( '.college-costs' ).offsetTop );
}

/**
 * _handleNavButtonClick - Handle click event for secondary nav.
 * @param {MouseEvents} event - click event object.
 */
function _handleNavButtonClick( event ) {
  event.preventDefault();
  if ( getStateValue( 'schoolErrors' ) === 'yes' ) {
    updateState.byProperty( 'showSchoolErrors', 'yes' );
    window.scrollTo( 0, document.querySelector( '.college-costs' ).offsetTop );
  } else {
    const target = event.target;
    sendAnalyticsEvent( 'Secondary nav click', event.target.innerText );

    if ( typeof target.dataset.nav_item !== 'undefined' ) {
      updateState.activeSection( target.dataset.nav_item );
    } else if ( typeof target.dataset.nav_section !== 'undefined' ) {
      closest( target, '[data-nav-is-open]' ).setAttribute( 'data-nav-is-open', 'True' );
    }
  }
}

/**
 * _handleNextButtonClick - handle the click event for the "Next" button.
 * @param {MouseEvent} event - click event object.
 */
function _handleNextButtonClick( event ) {
  // Check if there are missing form fields
  if ( getStateValue( 'schoolErrors' ) === 'yes' ) {
    updateState.byProperty( 'showSchoolErrors', 'yes' );
  } else {
    // TODO: Track time between Next button clicks for analytics
    sendAnalyticsEvent( 'next step - ' + getStateValue( 'activeSection' ), 'time-to-click' );
    updateState.nextSection();
    window.scrollTo( 0, document.querySelector( '.college-costs' ).offsetTop );
  }
}

export {
  navigationView
};
