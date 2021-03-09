import { scrollIntoView } from '../../../js/modules/util/scroll';
import DT from '../../owning-a-home/js/form-explainer/dom-tools';
import Expandable from '@cfpb/cfpb-expandables/src/Expandable.js';
import { assign } from '../../../js/modules/util/assign';
import { closest } from '@cfpb/cfpb-atomic-component/src/utilities/dom-traverse.js';


const CSS = {
  HAS_ATTENTION:         'has-attention',
  HOVER_HAS_ATTENTION:   'hover-has-attention'
};

const NO_OP = () => {
  // Placeholder function meant to be overridden.
};

let UNDEFINED;

/**
 * FormExplainer
 * @class
 *
 * @classdesc Initializes a new Form Explainer.
 *
 * @param {HTMLNode} element - Base DOM element.
 * @param {Object} options - Configuration options.
 * @returns {Object} An Form Explainer instance.
 */
class FormExplainer {
  constructor( element, options = {} ) {
    this.currentPage = options.currentPage || 1;
    this.elements = {};
  }

  /**
   * Initialize the FormExplainer.
   * @returns {FormExplainer} An instance.
   */
  init() {
    this.setPageCount();
    this.setCurrentPage( this.currentPage, UNDEFINED, false );
    this.setUIElements();
    this.initializeUI( this.elements );
    this.initializeEvents();

    return this;
  }

  /**
   * Initialize the UI after instatiation.
   * @param {HTMLNodes} elements - Current page DOM elements.
   */
  initializeUI( elements ) {
    if ( this.pageCount === 1 ) {
      DT.hide( '.form-explainer_page-buttons' );
    }

    DT.applyAll(
      elements.pages,
      ( value, index ) => {
        const _index = index + 1;
        if ( _index > 1 ) {
          // Hide all but the first parge
          const _page = this.getPageEl( _index );
          DT.hide( _page );
        }
      }
    );

    // eslint-disable-next-line global-require
    Expandable.init();
  }


  /**
   * Update the pagination UI.
   */
  updatePaginationUI( ) {
    const BTN_DISABLED = 'a-btn__disabled';
    const PAGE_BTN_CTR = '.form-explainer_page-buttons';


    if ( this.pageCount > 1 ) {
      DT.removeClass( PAGE_BTN_CTR + ' button', BTN_DISABLED );
      if ( this.currentPage === 1 ) {
        DT.addClass( PAGE_BTN_CTR + ' .prev', BTN_DISABLED );
      } else if ( this.currentPage === this.pageCount ) {
        DT.addClass( PAGE_BTN_CTR + ' .next', BTN_DISABLED );
      }
    }
  }

  /* Update attention classes based on the expandable or image overlay
   that was targeted.
   Remove the attention class from all the expandables/overlays,
   and then apply it to the target & its associated overlay
   or expandable.
   * @param {HTMLNode} target - Overlay or expandable DOM node.
   * @param {string} className - Hover class name.
   */
  updateAttention( target, className ) {
    let associated;
    const targetId = target.getAttribute( 'id' );

    DT.removeClass(
      '.o-expandable__form-explainer, .image-map_overlay',
      className
    );

    if ( target.getAttribute( 'href' ) !== null ) {
      associated = DT.getEl( target.getAttribute( 'href' ) );
    } else if ( targetId !== null ) {
      associated = DT.getEl( '[href="#' + targetId + '"]' );
    }

    if ( associated !== null ) {
      if ( className === CSS.HAS_ATTENTION ) {
        DT.removeClass( target, CSS.HOVER_HAS_ATTENTION );
        DT.removeClass( associated, CSS.HOVER_HAS_ATTENTION );
      }
      DT.addClass( target, className );
      DT.addClass( associated, className );
    }
  }

  /**
   * Open the expandable and scroll into the viewport.
   * @param {HTMLNode} imageOverlay - Image overlay, which was clicked.
   * @param {HTMLNode} targetExpandable - Target expandable.
   * current focus.
   */
  openAndScrollToExpandable( imageOverlay, targetExpandable ) {
    const targetExpandableTarget = targetExpandable.querySelector(
      '.o-expandable_target'
    );

    window.setTimeout( () => {
      scrollIntoView(
        targetExpandableTarget,
        { duration: 500, callback: () => targetExpandableTarget.focus() }
      );
    }, 150 );
    window.setTimeout( () => targetExpandableTarget.click(), 0 );
  }

  /**
   * Set the UI elements for the page
   * @returns {Object} DOM elements for the page.
   */
  setUIElements() {
    const explain = DT.getEl( '.explain' );
    const explainPagination = explain.querySelector( '.explain_pagination' );
    const explainPageBtns = explain.querySelectorAll(
      '.form-explainer_page-buttons button'
    );
    const pages = explain.querySelectorAll( '.explain_page' );
    const formExplainerLinks = explain.querySelectorAll(
      '.form-explainer_page-link'
    );

    return assign( this.elements,
      { explain,
        explainPageBtns,
        explainPagination,
        formExplainerLinks,
        pages
      }
    );
  }

  /**
   * Return explainer page element based on page number.
   * @param {number} pageNum - Number of explainer page.
   * @returns {Object} Page DOM element.
   */
  getPageEl( pageNum ) {
    return DT.getEl( `#explain_page-${ pageNum }` );
  }

  /**
   * Paginate through the various form pages.
   * @param {string} direction - 'next' or 'prev'.
   */
  paginate( direction ) {
    const currentPage = this.currentPage;
    const increment = direction === 'next' ? 1 : -1;
    const newPage = currentPage + increment;

    // Move to the next or previous page if it's not the first or last page.
    if ( ( direction === 'next' && newPage <= this.pageCount ) ||
         ( direction === 'prev' && newPage >= 1 ) ) {
      this.switchPage( currentPage, newPage );
    }
  }

  /**
   * Paginate through the various form pages.
   * @param {number} pageNum - Number of the current page.
   * @param {function} callback - Function to invode after scroll.
   * @param {boolean} shouldScrollIntoView - Whether to scroll the page into view.
   */
  setCurrentPage( pageNum, callback, shouldScrollIntoView = true ) {
    const CURRENT_PAGE = 'current-page';
    const PAGE_LINK = '.form-explainer_page-link';
    const PAGINATION = '.explain_pagination';
    const CURRENT_PAGE_LINK =
      '.form-explainer_page-link[data-page="' + pageNum + '"]';

    this.currentPage = parseInt( pageNum, 10 );

    DT.removeClass( PAGE_LINK, CURRENT_PAGE );
    DT.addClass( CURRENT_PAGE_LINK, CURRENT_PAGE );
    this.updatePaginationUI();

    if ( shouldScrollIntoView ) {
      scrollIntoView(
        DT.getEl( PAGINATION ),
        { duration: 200,
          callback: callback || NO_OP
        }
      );
    }
  }

  /**
   * Paginate through the various form pages.
   * @param {number} pageCount - Number of pages.
   */
  setPageCount( pageCount ) {
    const pages = DT.getEls( '.explain_page' );
    this.pageCount = pageCount || pages.length;
  }

  /**
   * Switch pages by fading pages in / out and
   * updating the UI accordingly.
   * @param {number} currentPage - Current page Number.
   * @param {number} newPage - New page number.
   */
  switchPage( currentPage, newPage ) {
    this.setCurrentPage( newPage, () => {
      // After scrolling the window, fade out the current page.
      DT.fadeOut( this.getPageEl( currentPage ), 600,
        () => {
          DT.fadeIn( this.getPageEl( newPage ), 700 );
        } );
    } );
  }

  /* Initialize the DOM events for the entire explainer UI. */
  initializeEvents() {
    const uiElements = this.elements;
    const delay = 700;

    if ( this.pageCount > 1 ) {

      /* When a paginantion link is clicked,
       * switch to the next / previous page.
       */
      DT.bindEvents( uiElements.explainPageBtns, 'click', event => {
        const target = event.currentTarget;

        if ( !DT.hasClass( target, 'disabled' ) ) {
          const direction = DT.hasClass( target, 'prev' ) ? 'prev' : 'next';
          this.paginate( direction );
        }
      } );

      /* When a page navigation link is clicked,
       * switch to the appropriate page.
       */
      DT.bindEvents( uiElements.formExplainerLinks, 'click', event => {
        const target = event.currentTarget;
        const pageNum = target.getAttribute( 'data-page' );
        const currentPage = this.currentPage;

        if ( !DT.hasClass( target, 'disabled' ) &&
             pageNum !== currentPage ) {
          this.switchPage( currentPage, pageNum );
        }
      } );
    }


    /* When the mouse is over the image overlay or form explainer,
     * update the hover styles.
     */
    DT.bindEvents(
      '.image-map_overlay, .o-expandable__form-explainer',
      [ 'mouseenter', 'mouseleave' ],
      event => {
        event.preventDefault();
        this.updateAttention( event.target, CSS.HOVER_HAS_ATTENTION );
      }
    );

    /* When a form explainer expandable target has the focus,
     * update the image overlay.
     */
    DT.bindEvents(
      '.o-expandable_target',
      'focus',
      event => {
        const expandable = closest(
          event.target,
          '.o-expandable__form-explainer'
        );
        this.updateAttention( expandable, CSS.HOVER_HAS_ATTENTION );
      }
    );

    /* When an overlay is clicked, toggle the corresponding expandable
     * and scroll the page until it is in view.
     */
    DT.bindEvents(
      '.image-map_overlay',
      'click',
      event => {
        event.preventDefault();
        event.stopPropagation();
        const imageOverlay = event.target;
        const itemID = imageOverlay.getAttribute( 'href' );
        const targetExpandable = DT.getEl( itemID );

        this.openAndScrollToExpandable( imageOverlay, targetExpandable );
      }
    );

    /* When a form explainer expandable is clicked / pressed,
     * update the image overlay position and hover styles.
     */
    DT.bindEvents(
      '.o-expandable__form-explainer .o-expandable_target',
      [ 'click', 'keypress' ],
      event => {
        if ( event.which === 13 || event.type === 'click' ) {
          const target = event.target;
          const closestFormExplainer = closest(
            target, '.o-expandable__form-explainer'
          );

          this.updateAttention( closestFormExplainer, CSS.HAS_ATTENTION );
        }
      }
    );
  }
}

export default FormExplainer;
