import Expandable from 'cf-expandables/src/Expandable';
import { bindEvent } from '../../../js/modules/util/dom-events';
import { queryOne as find } from '../../../js/modules/util/dom-traverse';
import { sendEvent } from './analytics';

const navHeader = find( '.o-regs3k-navigation_header' );
const navItems = find( '.o-regs3k-sections' );

const toggleSecondaryNav = () => {
  navHeader.classList.toggle( 'o-expandable_target__collapsed' );
  navHeader.classList.toggle( 'o-expandable_target__expanded' );
  navItems.classList.toggle( 'u-hide-on-stacked' );
};

const handleNavClick = event => {
  if ( !event.target.href ) {
    return;
  }
  // Double check that the URL ends in regulations/1234/XXXXXX
  let section = event.target.href.match( /regulations\/(\d+\/[\w\-]+)\/?$/ );
  if ( !section ) {
    return;
  }
  section = section[1].replace( '/', '-' );
  sendEvent( 'toc:click', section );
};

const bindSecondaryNav = () => {
  bindEvent( navHeader, {
    click: toggleSecondaryNav
  } );
};

const bindAnalytics = () => {
  bindEvent( navItems, {
    click: handleNavClick
  } );
};

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
};

Expandable.init();

window.addEventListener( 'load', init );
