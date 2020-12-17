import {
  scrollIntoView,
  scrollTo
} from '../../../../js/modules/util/scroll';
import DT from './dom-tools';
import Expandable from '@cfpb/cfpb-expandables/src/Expandable.js';
import { assign } from '../../../../js/modules/util/assign';
import { closest } from '@cfpb/cfpb-atomic-component/src/utilities/dom-traverse.js';
import throttle from 'lodash.throttle';

const EXPLAIN_TYPES = {
  CHECKLIST:   'checklist',
  DEFINITIONS: 'definitions'
};

const CSS = {
  EXPLAIN_PAGE_FIXED:    'explain_page__fixed',
  EXPLAIN_PAGE_ABSOLUTE: 'explain_page__absolute',
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
    this.elements.base = element;
    this.pageName = 'form';
    this.resized = false;
  }

  /**
   * Initialize the FormExplainer.
   * @returns {FormExplainer} An instance.
   */
  init() {
    this.setPageCount();
    this.setCurrentPage( this.currentPage, UNDEFINED, false );
    this.setUIElements();
    this.setTabIndex();
    this.initializeUI( this.elements );
    this.initializeEvents();

    return this;
  }

  /**
   * Initialize the UI after instatiation.
   * @param {HTMLNodes} elements - Current page DOM elements.
   */
  initializeUI( elements ) {
    this.updatePageUI( elements.initialTab, EXPLAIN_TYPES.CHECKLIST );

    if ( this.pageCount === 1 ) {
      DT.hide( '.form-explainer_page-buttons' );
    }

    DT.applyAll(
      elements.pages,
      ( value, index ) => {
        const _index = index + 1;
        this.updateImageUI( _index, true );
        this.setExplainerPlaceholders( _index );
      }
    );

    // eslint-disable-next-line global-require
    Expandable.init();
  }

  /**
   * Update the image UI for the current page.
   * @param {number} pageNum - Current page number.
   * @param {boolean} isPageLoad - Whether this is the initial page load.
   */
  updateImageUI( pageNum, isPageLoad ) {
    const elements = this.getPageElements( pageNum );

    if ( window.innerWidth > 600 ) {

      /* update widths & position on larger screens
         we only pass in the pageNum on pageLoad, when
         pages after the first will be hidden once they're
         fully loaded & we've calculated their widths */
      this.fitAndStickToWindow( elements, isPageLoad ? pageNum : null );
    } else if ( !isPageLoad ) {

      /* if this is called on screen resize instead of page load,
         remove width values & call unstick on the imageWrapper */
      elements.imageMapWrapper.style.width = '';
      DT.removeClass( elements.imageMapWrapper, CSS.EXPLAIN_PAGE_FIXED );
      elements.imageMap.style.width = '';
      elements.imageMapImage.style.width = '';
      DT.applyAll( elements.terms, element => ( element.style.width = '' ) );
      DT.removeClass( elements.imageMapWrapper, CSS.EXPLAIN_PAGE_FIXED );
    } else if ( pageNum > 1 ) {

      // on page load, hide pages except first
      DT.hide( elements.page );
    }
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

  /**
   * Update the page UI for the give explainer type.
   * @param {string} currentTab - Name of current tab.
   * @param {string} explainerType - Type of form explainer.
   */
  updatePageUI( currentTab, explainerType ) {
    this.updateTabsUI( currentTab );

    DT.hide( '.o-expandable__form-explainer' );
    DT.show( '.o-expandable__form-explainer-' + explainerType );
    DT.hide( '.image-map_overlay' );
    DT.show( '.image-map_overlay__' + explainerType );
  }

  /**
   * Update the tabs UI.
   * @param {string} currentTab - Name of current tab.
   */
  updateTabsUI( currentTab ) {

    // Update the tab state
    DT.removeClass( '.explain_tabs .tab-list', 'active-tab' );
    DT.addClass( currentTab, 'active-tab' );
  }

  /**
   * Update the image position, with possible delay.
   * @param {number} delay - Time delay before updating the image position.
   */
  updateImagePositionAfterAnimation( delay = 0 ) {
    setTimeout( () => {
      if ( window.innerWidth > 600 ) {
        DT.nextFrame( this.updateStickiness.bind( this ) );
      }
    }, delay );
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
   * Return page elements based on the page number.
   * @param {Object} pageNum - Current page number.
   * @returns {Object} DOM elements for the page.
   */
  getPageElements( pageNum ) {
    const element = this.getPageEl( pageNum );

    return {
      page: element,
      imageMap: element.querySelector( '.image-map' ),
      imageMapImage: element.querySelector( '.image-map_image' ),
      imageMapWrapper: element.querySelector( '.image-map_wrapper' ),
      terms: element.querySelectorAll( '.terms' )
    };
  }

  /**
   * Set the UI elements for the page
   * @returns {Object} DOM elements for the page.
   */
  setUIElements() {
    const explain = DT.getEl( '.explain' );
    const explainTabs = explain.querySelector( '.explain_tabs' );
    const explainPagination = explain.querySelector( '.explain_pagination' );
    const explainPageBtns = explain.querySelectorAll(
      '.form-explainer_page-buttons button'
    );
    const tabLink = explain.querySelector(
      '.tab-link[data-target="' + EXPLAIN_TYPES.CHECKLIST + '"]'
    );
    const initialTab = closest( tabLink, '.tab-list' );
    const tabList = explain.querySelectorAll( '.explain_tabs .tab-list' );
    const pages = explain.querySelectorAll( '.explain_page' );
    const formExplainerLinks = explain.querySelectorAll(
      '.form-explainer_page-link'
    );

    return assign( this.elements,
      { explain,
        explainPageBtns,
        explainPagination,
        explainTabs,
        formExplainerLinks,
        initialTab,
        pages,
        tabLink,
        tabList
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
   * Calculate the new image width based on the height of the window.
   * @param {number} imageWidth - Width of the image.
   * @param {number} imageHeight - Height of the image.
   * @param {number} windowHeight - Height of the window.
   * @returns {Object} Page DOM element.
   */
  calculateNewImageWidth( imageWidth, imageHeight, windowHeight ) {
    const imageMapImageRatio = ( imageWidth + 2 ) / ( imageHeight + 2 );

    return ( ( windowHeight - 60 ) * imageMapImageRatio ) + 30;
  }

  /**
   * Resize the image map and corresponding images, based on window size.
   * @param {HTMLNodes} elements - Current page DOM elements.
   * @param {boolean} windowResize - Whether the images are being resized
   * based on a window resize event.
   */
  resizeImage( elements, windowResize ) {
    const pageWidth = elements.page.clientWidth;
    const imageMapImage = elements.imageMapImage;
    const currentHeight = imageMapImage.clientHeight;
    const currentWidth = imageMapImage.clientWidth;
    const actualWidth = imageMapImage.getAttribute( 'data-actual-width' );
    const actualHeight = imageMapImage.getAttribute( 'data-actual-height' );
    const windowHeight = window.innerHeight - 60;
    let newWidth;
    let newWidthPercentage;

    /* If the image is too tall for the window, resize it proportionally,
       then update the adjacent terms column width to fit.
       On window resize, also check if image is now too small & resize,
       but only if we've stored the actual image dimensions for comparison. */
    if ( ( currentHeight > windowHeight ) ||
         ( windowResize && actualWidth && actualHeight ) ) {
      // determine new width
      newWidth = this.calculateNewImageWidth(
        currentWidth, currentHeight, window.innerHeight
      );

      if ( actualWidth && newWidth > actualWidth ) {
        newWidth = actualWidth;
      }

      // update element widths
      newWidthPercentage = newWidth / pageWidth * 100;

      /* on screen less than 800px wide, the terms need a minimum 33%
         width or they become too narrow to read */
      if ( window.innerWidth <= 800 && newWidthPercentage > 67 ) {

        newWidthPercentage = 67;
      }

      elements.imageMap.style.width = newWidthPercentage + '%';

      DT.applyAll(
        elements.terms,
        element => ( element.style.width = 100 - newWidthPercentage + '%' )
      );
    }
  }

  /**
   * Set the image map and image map widths, in pixels.
   * @param {HTMLNodes} elements - Current page DOM elements.
   */
  setImageElementWidths( elements ) {

    /* When the image position is set to `fixed`,
       it no longer constrained to its parent.
       To fix this we will give it its own width that is equal to the parent.
       (IE8 wants a width on the wrapper too) */
    const containerWidth = elements.imageMap.clientWidth + 'px';
    elements.imageMapImage.style.width = containerWidth;
    elements.imageMapWrapper.style.width = containerWidth;
  }

  /**
   * Store the image widths in data attributes.
   * @param {Object} image - Current form explainer image map.
   */
  storeImageDimensions( image ) {
    image.setAttribute( 'data-actual-width', image.clientWidth );
    image.setAttribute( 'data-actual-height', image.clientHeight );
  }

  /**
   * Limit .image-map_image to the height of the window and then adjust the two
   * columns to match.
   * @param {HTMLNodes} elements - Current page DOM elements.
   * @param {number} pageNum - Current page number.
  */
  fitAndStickToWindow( elements, pageNum ) {
    if ( pageNum ) {
      this.storeImageDimensions( elements.imageMapImage );
    }

    this.resizeImage( elements, !pageNum );

    // set width values on image elements
    this.setImageElementWidths( elements );

    this.updateStickiness();

    // show the first page
    if ( pageNum > 1 ) {
      DT.hide( elements.page );
    }
  }

  /**
   * Modify the image position if the viewport has been scrolled past
   * current page, so that the sticky element does not overlap
   * content that comes after current page.
   */
  updateStickiness( ) {
    const imageMapWrapper = this.elements.imageMapWrapper;
    const page = this.elements.currentPage;
    const pageBottom = window.pageYOffset +
                       page.getBoundingClientRect().bottom -
                       imageMapWrapper.offsetHeight;
    const yPos = imageMapWrapper.parentNode.getBoundingClientRect().top;

    if ( yPos < 30 ) {
      if ( window.pageYOffset >= pageBottom ) {
        DT.removeClass( imageMapWrapper, CSS.EXPLAIN_PAGE_FIXED );
        DT.addClass( imageMapWrapper, CSS.EXPLAIN_PAGE_ABSOLUTE );
      } else {
        DT.removeClass( imageMapWrapper, CSS.EXPLAIN_PAGE_ABSOLUTE );
        DT.addClass( imageMapWrapper, CSS.EXPLAIN_PAGE_FIXED );
      }
    } else {
      DT.removeClass( imageMapWrapper, CSS.EXPLAIN_PAGE_FIXED );
      DT.removeClass( imageMapWrapper, CSS.EXPLAIN_PAGE_ABSOLUTE );
    }
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
    this.elements.currentPage = this.getPageEl( pageNum );
    assign( this.elements, this.getPageElements( pageNum ) );

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
          this.updateImageUI( newPage );
        } );
    } );
  }

  /**
   * Unset the image position by removing the appropriate classes.
   */
  unStickImage() {
    const element = this.getPageEl( this.currentPage );

    DT.removeClass( element, CSS.EXPLAIN_PAGE_FIXED );
    DT.removeClass( element, CSS.EXPLAIN_PAGE_ABSOLUTE );
  }

  /**
   * Add the scroll event listener and set the image position.
   */
  stickImage() {
    window.removeEventListener( 'scroll', this.onScroll );
    if ( window.innerWidth > 600 ) {
      this.onScroll = throttle( () => {
        this.updateStickiness();
      }, 100 );
      window.addEventListener( 'scroll', this.onScroll );
    } else {
      this.unStickImage();
    }
  }

  /**
   * Set explainer placeholders.
   * @param {string} id - ID of the current page.
   */
  setExplainerPlaceholders( id ) {
    const page = this.getPageEl( id );
    let placeholder;
    Object.keys( EXPLAIN_TYPES ).forEach( key => {
      const category = EXPLAIN_TYPES[key];
      if ( !this.explainerHasContent( page, category ) ) {
        placeholder = this.generatePlaceholderHtml( category, this.pageName );
        page.querySelector( '.explain_terms ' ).appendChild( placeholder );
      }
    } );
  }

  /**
   * Generate explainer placeholder HTML.
   * @param {string} explainerType - Type of form explainer.
   * @param {string} pageName - Name of the page.
   * @returns {HTMLNode} Placeholder DOM node.
   */
  generatePlaceholderHtml( explainerType, pageName ) {
    const HTML =
      '<div class="o-expandable o-expandable__padded' +
      ' o-expandable__form-explainer ' +
      'o-expandable__form-explainer-' + explainerType + ' ' +
      'o-expandable__form-explainer-placeholder">' +
      '<span class="o-expandable_header">' +
      'Click on ' +
      '"Get Definitions" above or page ahead to continue checking your ' +
      pageName + '.</span></div>';

    return DT.createElement( HTML );
  }

  /**
   * Determine if the explainer has content.
   * @param {HTMLNode} page - Current page element.
   * @param {string} explainerType - Type form explainer.
   * @returns {boolean} Whether the explainer has content.
   */
  explainerHasContent( page, explainerType ) {
    return page.querySelector(
      '.o-expandable__form-explainer-' + explainerType
    ) !== null;
  }

  /**
   * Set the tab index to 0 for all form explainer links.
   */
  setTabIndex() {
    const elements = DT.getEls(
      '.o-expandable__form-explainer .o-expandable_content a'
    );

    DT.applyAll(
      elements,
      element => element.setAttribute( 'tabindex', 0 )
    );
  }

  /* Initialize the DOM events for the entire explainer UI. */
  initializeEvents() {
    const uiElements = this.elements;
    const delay = 700;

    this.stickImage();

    window.addEventListener(
      'resize',
      throttle( () => {
        this.updateImageUI( this.currentPage );
        this.stickImage();
      }, 250 )
    );

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

    /* When the tab list is clicked,
     * scroll it into view and update the page UI.
     */
    DT.bindEvents( uiElements.tabList, 'click', event => {
      const selectedTab = event.currentTarget;
      const explainerType = selectedTab.querySelector( '[data-target]' )
        .getAttribute( 'data-target' );
      this.updatePageUI( selectedTab, explainerType );

      scrollTo(
        uiElements.tabList[0].getBoundingClientRect().top +
        window.pageYOffset,
        {
          duration: 300,
          offset: -30
        }
      );
    } );

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
          this.updateImagePositionAfterAnimation( 600 );
        }
      }
    );
  }
}

export default FormExplainer;
