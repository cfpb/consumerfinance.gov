import Expandable from 'cf-expandables/src/Expandable';
import { bindEvent } from '../../../js/modules/util/dom-events';
import { queryOne as find } from '../../../js/modules/util/dom-traverse';
import { handleContentClick, handleNavClick } from './analytics';
import * as utils from './regs3k-utils';

const navHeader = find( '.o-regs3k-navigation_header' );
const navItems = find( '.o-regs3k-sections' );
const regContent = find( '.content_main.regulations3k' );


/**
 * toggleSecondaryNav - Show/hide the secondary nav on smaller screens
 */
const toggleSecondaryNav = () => {
  navHeader.classList.toggle( 'o-expandable_target__collapsed' );
  navHeader.classList.toggle( 'o-expandable_target__expanded' );
  navItems.classList.toggle( 'u-hide-on-stacked' );
};

/**
 * bindSecondaryNav - Set up secondary nav toggling.
 */
const bindSecondaryNav = () => {
  bindEvent( navHeader, {
    click: toggleSecondaryNav
  } );
};

/**
 * bindAnalytics - Set up analytics reporting.
 */
const bindAnalytics = () => {
  bindEvent( navItems, {
    click: handleNavClick
  } );
  bindEvent( regContent, {
    click: handleContentClick
  } );
};

/**
 * init - Initialize everything on page load.
 */
const init = () => {
  if ( 'serviceWorker' in navigator ) {
    navigator.serviceWorker.register( '/regulations3k-service-worker.js' ).catch( err => {
      console.error( 'Error during service worker registration:', err );
    } );
  }
  if ( navHeader ) {
    navHeader.classList.add( 'o-expandable_target__collapsed' );
    navItems.classList.add( 'u-hide-on-stacked' );
    bindSecondaryNav();
    bindAnalytics();
  }
  if ( utils.isOldHash( window.location.hash ) ) {
    window.location.hash = utils.getNewHash( window.location.hash );
  }
};

Expandable.init();

window.addEventListener( 'load', init );
