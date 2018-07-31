import Expandable from 'cf-expandables/src/Expandable';
import { bindEvent } from '../../../js/modules/util/dom-events';
import { queryOne as find } from '../../../js/modules/util/dom-traverse';

const navHeader = find( '.o-regs3k-navigation_header' );
const navItems = find( '.o-regs3k-sections' );

const toggleSecondaryNav = () => {
  navHeader.classList.toggle( 'o-expandable_target__collapsed' );
  navHeader.classList.toggle( 'o-expandable_target__expanded' );
  navItems.classList.toggle( 'u-hide-on-stacked' );
};

const bindSecondaryNav = () => {
  bindEvent( navHeader, {
    click: toggleSecondaryNav
  } );
};

const init = () => {
  if ( 'serviceWorker' in navigator ) {
    navigator.serviceWorker.register( '/regulations3k-service-worker.js' ).catch( err => {
      console.error( 'Error during service worker registration:', err );
    } );
  }
  navItems.classList.toggle( 'u-hide-on-stacked' );
  bindSecondaryNav();
};

Expandable.init();

window.addEventListener( 'load', init );
