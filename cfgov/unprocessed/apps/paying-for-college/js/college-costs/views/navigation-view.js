// This file contains the 'view' of all financial info, including costs, loans, etc

import {
  getAllStateValues,
  getStateValue,
} from '../dispatchers/get-model-values.js';
import { sendAnalyticsEvent } from '../util/analytics.js';
import { updateFinancialViewAndFinancialCharts } from '../dispatchers/update-view.js';
import { updateState } from '../dispatchers/update-state.js';

const navigationView = {
  _contentSidebar: null,
  _introduction: null,
  _sections: null,
  _navMenu: null,
  _navListItems: null,
  _navItems: null,
  _SecondaryNavButtons: null,
  _navButtons: null,
  _appSegment: null,
  _stateDomElem: null,
  _affordingChoices: null,

  /**
   * _handlePopState - handle popstate events
   * @param {object} event - the popstate event
   */
  _handlePopState: function (event) {
    if (event.state) {
      const values = getAllStateValues();
      values.activeSection = event.state.activeSection;
      updateState.replaceStateInHistory(window.location.search);
      updateState.activeSection(values.activeSection, true);
    }
  },

  /**
   * _updateSideNav - Update the side nav
   * @param {string} activeName - name of the active app section
   */
  _updateSideNav: function (activeName) {
    if (typeof activeName === 'undefined') {
      activeName = getStateValue('activeSection');
    }
    // clear active-sections
    navigationView._navItems.forEach((elem) => {
      elem.classList.remove('active-section');
      elem.setAttribute('aria-selected', false);
    });

    const navItem = document.querySelector(
      '[data-nav_section="' + activeName + '"]',
    );
    if (navItem === null) return;
    const activeElem = navItem.closest('li');
    // const activeParent = activeElem.closest(
    //   '.o-secondary-nav__list-item--parent',
    // );

    this._navListItems.forEach((elem) => {
      elem.setAttribute('data-nav-is-active', 'False');
      elem.setAttribute('data-nav-is-open', 'False');
    });

    activeElem.setAttribute('data-nav-is-active', 'True');
    activeElem.setAttribute('aria-selected', true);
    // activeParent.setAttribute('data-nav-is-open', 'True');
    // activeParent.setAttribute('data-nav-is-active', 'True');
    // activeElem.setAttribute('aria-selected', true);
    // activeParent
    //   .querySelectorAll('.o-secondary-nav__list--children li')
    //   .forEach((elem) => {
    //     elem.setAttribute('data-nav-is-active', 'True');
    //   });

    navItem.classList.add('active-section');
  },

  /**
   * _showAndHideSections - Hide all app sections, then show appropriate ones
   * @param {string} activeName - Name of the active section
   */
  _showAndHideSections: function (activeName) {
    const query =
      '.college-costs__tool-section[data-tool-section="' + activeName + '"]';
    const activeSection = document.querySelector(query);

    this._sections.forEach((elem) => {
      elem.classList.remove('active');
    });

    activeSection.classList.add('active');
  },

  /**
   * updateView - Public method to run private update methods
   */
  updateView: function () {
    const started = getStateValue('gotStarted');
    const activeName = getStateValue('activeSection');
    if (started && activeName) {
      this._updateSideNav(activeName);
      this._showAndHideSections(activeName);
      this._updateViewCallback(activeName);
    }
  },

  /**
   * updateStateInDom - manages dataset for the MAIN element, which helps display UI elements
   * properly
   * @param {string} property - The state property to modify
   * @param {string} value - The new value of the property
   * NOTE: if the value is null or the Boolean 'false', the data attribute will be removed
   */
  updateStateInDom: function (property, value) {
    if (value === false || value === null) {
      navigationView._stateDomElem.removeAttribute('data-state_' + property);
    } else {
      navigationView._stateDomElem.setAttribute(
        'data-state_' + property,
        value,
      );
    }
  },

  /**
   * init - Initialize the navigation view
   * @param {object} body - The body element of the page
   * @param { string } iped - String representing the chosen school.
   * @param {Function} updateViewCallback - = A function called when the view updates
   */
  init: function (body, iped, updateViewCallback) {
    this._navMenu = body.querySelector('.o-secondary-nav');
    this._SecondaryNavButtons = body.querySelectorAll('.o-secondary-nav a');
    this._navListItems = body.querySelectorAll('.o-secondary-nav li');
    this._navItems = body.querySelectorAll('[data-nav_item]'); 
    this._navButtons = body.querySelectorAll(
      '.college-costs__tool-section-buttons .btn__nav',
    );
    this._contentSidebar = body.querySelector('.content__sidebar');
    this._introduction = body.querySelector('.college-costs__intro-segment');
    this._getStartedBtn = body.querySelector(
      '.college-costs__intro-segment .btn__get-started',
    );
    this._appSegment = body.querySelector('.college-costs__app-segment');
    this._sections = body.querySelectorAll('.college-costs__tool-section');
    this._stateDomElem = document.querySelector('main.college-costs');
    this._affordingChoices = document.querySelectorAll(
      '.affording-loans-choices .m-form-field',
    );
    this._updateViewCallback = updateViewCallback;

    _addButtonListeners(iped);
    this.updateView();

    updateState.replaceStateInHistory(window.location.search);
    window.addEventListener('popstate', navigationView._handlePopState);
  },
};

/**
 * _addButtonListeners - Add event listeners for nav buttons
 * @param { string } iped - String representing the chosen school.
 */
function _addButtonListeners(iped) {
  navigationView._SecondaryNavButtons.forEach((elem) => {
    elem.addEventListener('click', _handleSecondaryNavButtonClick);
  });

  navigationView._affordingChoices.forEach((elem) => {
    elem.addEventListener('click', _handleAffordingChoicesClick);
  });

  navigationView._navButtons.forEach((elem) => {
    elem.addEventListener('click', _handleNavButtonClick);
    if (iped) {
      _handleGetStartedBtnClick();
    } else {
      navigationView._getStartedBtn.addEventListener(
        'click',
        _handleGetStartedBtnClick,
      );
    }
  });
}

/**
 * _handleAffordingChoicesClick - Handle clicks on Affording Payment choices.
 * @param {MouseEvent} event - The click event object.
 */
function _handleAffordingChoicesClick(event) {
  const parent = event.target.closest('.m-form-field');
  const input = parent.querySelector('input[name="affording-display-radio"]');
  updateState.byProperty('expensesChoice', input.value);
}

/**
 * _handleGetStartedBtnClick - Handle the click of the "Get Started" button.
 */
function _handleGetStartedBtnClick() {
  updateState.getStarted(true);
  updateState.activeSection('school-info');
  navigationView.updateView();
  // The user should be sent back to the top of the P4C content
  window.scrollTo(0, document.querySelector('.college-costs').offsetTop);
}

/**
 * _handleSecondaryNavButtonClick - Handle click event for secondary nav.
 * @param {MouseEvent} event - click event object.
 */
function _handleSecondaryNavButtonClick(event) {
  event.preventDefault();
  if (getStateValue('schoolErrors') === 'yes') {
    updateState.byProperty('showSchoolErrors', 'yes');
    window.scrollTo(0, document.querySelector('.college-costs').offsetTop);
  } else {
    const target = event.target;
    sendAnalyticsEvent('Secondary nav click', event.target.innerText);

    if ( typeof target.dataset.nav_section !== 'undefined' ) {
      updateState.activeSection( target.dataset.nav_section );
    }

    // if (typeof target.dataset.nav_item !== 'undefined') {
    //   updateState.activeSection(target.dataset.nav_item);
    // } else if (typeof target.dataset.nav_section !== 'undefined') {
    //   target
    //     .closest('[data-nav-is-open]')
    //     .setAttribute('data-nav-is-open', 'True');
    // }
  }
}

/**
 * _handleNavButtonClick - handle the click event for a nav button.
 * @param event
 */
function _handleNavButtonClick(event) {
  // Check if there are missing form fields
  if (getStateValue('schoolErrors') === 'yes') {
    updateState.byProperty('showSchoolErrors', 'yes');
  } else {
    const target = event.target;
    if (event.target.dataset.hasOwnProperty('destination')) {
      const destination = event.target.dataset.destination;
      sendAnalyticsEvent(
        'Navigation Button from ' +
          getStateValue('activeSection') +
          ' to ' +
          destination,
        'time-to-click',
      );
      if (destination === 'debt-at-grad') {
        updateFinancialViewAndFinancialCharts();
      }
      updateState.navigateTo(destination);
      window.scrollTo(0, document.querySelector('.college-costs').offsetTop);
      document.querySelector('.college-costs__tool-section.active h2').focus();
    }
  }
}

export { navigationView };
