// Required modules.
import { checkDom, setInitFlag } from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';
import GlobalSearch from '../molecules/GlobalSearch';
import MegaMenu from '../organisms/MegaMenu';

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
   * Check if either the mega menu or the global search is open.
   * @returns {Boolean} true if either the mega menu or the global search is open.
   */
  function _hasOpenMenu() {
    return document.querySelector( '.o-mega-menu_content' ).getAttribute( 'aria-expanded' ) === 'true' ||
           document.querySelector( '.m-global-search_content' ).getAttribute( 'aria-expanded' ) === 'true';
  }


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

    // Don't initialize the mega menu if it isn't on the page.
    if ( _dom.classList.contains( `${ BASE_CLASS }__mega-menu` ) ) {
      _megaMenu = new MegaMenu( _dom );
      _megaMenu.addEventListener( 'rootExpandBegin', _megaMenuExpandBegin );
      _megaMenu.addEventListener( 'rootCollapseEnd', _megaMenuCollapseEnd );
      _megaMenu.init();

      _globalSearch = new GlobalSearch( _dom );
      _globalSearch.addEventListener( 'expandBegin', _globalSearchExpandBegin );
      _globalSearch.addEventListener( 'collapseEnd', _globalSearchCollapseEnd );
      _globalSearch.init();
    }

    return this;
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
    if ( !_hasOpenMenu() ) {
      _overlay.classList.add( 'u-hidden' );
    }
  }

  /**
   * Handler for when the global search begins expansion.
   * Collapse the mega menu.
   */
  function _globalSearchExpandBegin() {
    _megaMenu.collapse();
    _overlay.classList.remove( 'u-hidden' );
  }

  /**
   * Handler for when the global search ends collapsing.
   * Show an overlay.
   */
  function _globalSearchCollapseEnd() {
    setTimeout( () => {
      if ( !_hasOpenMenu() ) {
        _overlay.classList.add( 'u-hidden' );
      }
    }, 100 );
  }

  this.init = init;

  return this;
}

export default Header;
