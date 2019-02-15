// Required modules.
import { checkDom, setInitFlag } from '../modules/util/atomic-helpers';
import GlobalSearch from '../molecules/GlobalSearch.js';
import MegaMenu from '../organisms/MegaMenu.js';

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
   * @returns {Header|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init( overlay ) {
    if ( !setInitFlag( _dom ) ) {
      let UNDEFINED;
      return UNDEFINED;
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
