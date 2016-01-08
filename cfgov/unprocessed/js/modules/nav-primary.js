/* ==========================================================================
   Desktop Menu Transitions
   Do not apply a transition when hovering from one menu to the next
   ========================================================================== */

'use strict';

var expandedState = require( './util/expanded-state' );
var domTraverse = require( './util/dom-traverse' );

var _primaryNav;
var _primaryTrigger;
var _primaryLinks;
var _subNavs;

/**
 * Set up DOM references and event handlers.
 */
function init() {
  _primaryNav = document.querySelector( '.js-primary-nav' );
  _primaryTrigger = document.querySelector( '.js-primary-nav_trigger' );
  _primaryLinks = _primaryNav.querySelectorAll( '.js-primary-nav_link' );
  _subNavs = _primaryNav.querySelector( '.js-sub-nav' );

  _primaryTrigger.addEventListener( 'click', _primaryTriggerAction );

  _primaryNav.addEventListener( 'click', _primaryLinkClicked );

  var subBack = _primaryNav.querySelector( '.js-sub-nav_back' );
  subBack.addEventListener( 'click', _subBackBtnClicked );

/*
  TODO: wrap in a breakpoint handler along with other hover
  events to open the menu after #907 is merged

  _primaryNav.addEventListener( 'mouseleave', function() {
    expandedState.toggleExpandedState( subNavs, false );
  } );
*/
}

/**
 * Handle a click of the button to close the submenu.
 *
 * @param {MouseEvent} event
 *   The event object for the click of the close button.
 */
function _subBackBtnClicked( event ) {
  var target = event.currentTarget;
  var targetSubNav = domTraverse.closest( target, 'js-sub-nav' );
  var targetPrimaryItem = domTraverse.closest( target, 'js-primary-nav_item' );
  targetPrimaryItem = targetPrimaryItem.querySelector( '.js-primary-nav_link' );
  expandedState.toggleExpandedState( _primaryLinks, 'false' );
  expandedState.toggleExpandedState( targetSubNav, 'false', function() {
    targetPrimaryItem.focus();
  } );
}

/**
 * Handle a click of primary trigger to open/close the nav menu.
 */
function _primaryTriggerAction() {
  if ( expandedState.isThisExpanded( _primaryNav ) ) {
    expandedState.toggleExpandedState( _primaryNav, 'false', function() {
      _primaryTrigger.focus();
    } );
  } else {
    expandedState.toggleExpandedState( _primaryNav, 'true', function() {
      _primaryLinks[0].focus();
    } );
  }

  expandedState.toggleExpandedState( _primaryTrigger );
}

/**
 * Handle a click of top-level link in the menu.
 *
 * @param {MouseEvent} event
 *   The event object for the click of a menu link.
 * @returns {undefined}
 *   Bail out of the method if the click is not on a nav_link.
 */
function _primaryLinkClicked( event ) {
  var target = event.target;
  if ( !target.classList.contains( 'js-primary-nav_link' ) ) {
    return;
  }

  event.preventDefault();
  event.stopImmediatePropagation();

  var targetSubNavs = domTraverse.getSiblings( target, '.js-sub-nav' );
  var otherSubNavs = domTraverse.not( _subNavs, targetSubNavs );
  var firstLink = targetSubNavs[0].querySelector( 'a' );

  if ( expandedState.isOneExpanded( otherSubNavs ) ) {
    expandedState.toggleExpandedState( _primaryLinks, 'false' );
    expandedState.toggleExpandedState(
      otherSubNavs,
      'false',
      function() {
        expandedState.toggleExpandedState( targetSubNavs );
        firstLink.focus();
      }
    );
  } else if ( expandedState.isOneExpanded( targetSubNavs ) ) {
    expandedState.toggleExpandedState( targetSubNavs, 'false', function() {
      target.focus();
    } );
  } else {
    expandedState.toggleExpandedState( targetSubNavs, null, function() {
      firstLink.focus();
    } );
  }

  expandedState.toggleExpandedState( target );
}

// Expose public methods.
module.exports = { init: init };
