// This file contains the 'view' of all financial info, including costs, loans, etc

import { closest } from '../../../../js/modules/util/dom-traverse';
import { updateState } from '../dispatchers/update-state.js';
import { getState } from '../dispatchers/get-state.js';
import { bindEvent } from '../../../../js/modules/util/dom-events';

const navigationView = {
  _contentSidebar: null,
  _introduction: null,
  _sections: null,
  _navMenu: null,
  _navListItems: null,
  _navButtons: null,
  _nextButtons: null,
  _feelingGauge: null,
  _appSegment: null,

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

    bindEvent( navigationView._getStartedBtn, { click: this._handleGetStartedBtnClick } );
    bindEvent( navigationView._feelingGauge, { click: this._handleFeelingGaugeEvent } );

  },

  _handleFeelingGaugeEvent: function( event ) {
    navigationView.activateGetStartedBtn();
  },

  _handleGetStartedBtnClick: function( event ) {
    updateState.getStarted( true );
    navigationView._introduction.classList.add( 'hidden' );
    navigationView._appSegment.classList.add( 'active' );
    updateState.activeSection( 'school-info' );
    // The user should be sent back to the top of the P4C content
    window.scrollTo( 0, document.querySelector( '.college-costs' ).offsetTop );
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
    updateState.activeSection( event.target.dataset.buttonTarget );
    // The user should be sent back to the top of the P4C content
    window.scrollTo( 0, document.querySelector( '.college-costs' ).offsetTop );

  },

  _updateSideNav: function( activeName ) {
    const navItem = navigationView._navMenu.querySelector( '[data-nav_item="' + activeName + '"]' );
    const activeElem = closest( navItem, 'li' );
    const activeParent = closest( activeElem, '.o-college-costs-nav__section' );
    this._navListItems.forEach( elem => {
      elem.classList.remove( 'active' );
    } );

    activeElem.classList.add( 'active' );
    activeParent.classList.add( 'active' );

  },

  _updateSection: function( activeName ) {
    const query = '.college-costs_tool-section[data-tool-section="' + activeName + '"]';
    const activeSection = document.querySelector( query );

    this._sections.forEach( elem => {
      elem.classList.remove( 'active' );
    } );

    activeSection.classList.add( 'active' );
  },

  activateGetStartedBtn: function() {
    this._getStartedBtn.classList.remove( 'a-btn__disabled' );
    this._getStartedBtn.removeAttribute( 'disabled' );
  },

  init: function( body ) {
    this._navMenu = body.querySelector( '.o-college-costs-nav' );
    this._navButtons = body.querySelectorAll( '.o-college-costs-nav button' );
    this._navListItems = body.querySelectorAll( '.o-college-costs-nav li' );
    this._nextButtons = body.querySelectorAll( '.college-costs_tool-section .btn__next-step' );
    this._contentSidebar = body.querySelector( '.content_sidebar' );
    this._introduction = body.querySelector( '.college-costs_intro-segment' );
    this._getStartedBtn = body.querySelector( '.college-costs_intro-segment .btn__get-started' );
    this._appSegment = body.querySelector( '.college-costs_app-segment' );
    this._sections = body.querySelectorAll( '.college-costs_tool-section' );
    this._feelingGauge = body.querySelector( '.college-costs .feeling-gauge' );

    this._addButtonListeners();

    this.update();

  },

  update: function() {
    const started = getState( 'gotStarted' );
    if ( started ) {
      const activeName = getState( 'activeSection' );
      this._updateSideNav( activeName );
      this._updateSection( activeName );
    }
    console.log( 'updated FinView' );
  }

};

export {
  navigationView
};
