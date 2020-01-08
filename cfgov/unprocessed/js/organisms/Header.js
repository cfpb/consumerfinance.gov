// Required modules.
import { checkDom, setInitFlag } from '../modules/util/atomic-helpers';
import GlobalSearch from '../molecules/GlobalSearch';
import MegaMenuOrig from '../organisms/MegaMenu';

/*
  TODO: Remove when 2019/2020 Mega Menu modifications are finalized.
  Global variables are set by a flag in the base template.
*/
let MegaMenu;
import MegaMenuVar1 from '../organisms/MegaMenuVar1';
import MegaMenuVar2 from '../organisms/MegaMenuVar2';

if ( window.cfpb && window.cfpb.megaMenuVar1 ) {
  MegaMenu = MegaMenuVar1;
} else if ( window.cfpb && window.cfpb.megaMenuVar2 ) {
  MegaMenu = MegaMenuVar2;
} else {
  MegaMenu = MegaMenuOrig;
}

/**
 * Header
 * @class
 *
 * @classdesc Initializes a new Header organism.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the organism.
 * @returns {Object} An Header instance.
 */
function Header( element ) {

  const BASE_CLASS = 'o-header';

  const _dom = checkDom( element, BASE_CLASS );

  let _globalSearch;
  let _megaMenu;
  let _overlay;

  /**
   * @param {HTMLNode} overlay
   *   Overlay to show/hide when mobile mega menu is shown.
   * @returns {Header} An instance.
   */
  function init( overlay ) {
    if ( !setInitFlag( _dom ) ) {
      return this;
    }

    // Semi-opaque overlay that shows over the content when the menu flies out.
    _overlay = overlay;

    _globalSearch = new GlobalSearch( _dom );
    _globalSearch.addEventListener( 'expandBegin', _searchExpandBegin );
    _globalSearch.init();

    _megaMenu = new MegaMenu( _dom );
    _megaMenu.addEventListener( 'rootExpandBegin', _megaMenuExpandBegin );
    _megaMenu.addEventListener( 'rootCollapseEnd', _megaMenuCollapseEnd );
    _megaMenu.init();

    return this;
  }

  /**
   * Handler for opening the search.
   */
  function _searchExpandBegin() {
    _megaMenu.collapse();
  }


  /**
   * Handler for when the mega menu begins expansion.
   * Collapse the global search.
   */
  function _megaMenuExpandBegin() {
    _globalSearch.collapse();
    _overlay.classList.remove( 'u-hidden' );
  }

  /**
   * Handler for when the mega menu ends collapsing.
   * Show an overlay.
   */
  function _megaMenuCollapseEnd() {
    _overlay.classList.add( 'u-hidden' );
  }

  this.init = init;

  return this;
}

export default Header;
