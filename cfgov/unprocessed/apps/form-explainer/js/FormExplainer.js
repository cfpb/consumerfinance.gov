import { scrollIntoView } from '../../../js/modules/util/scroll.js';
import DT from './dom-tools.js';
import { ExpandableGroup } from '@cfpb/cfpb-design-system';

const CSS = {
  HAS_ATTENTION: 'has-attention',
  HOVER_HAS_ATTENTION: 'hover-has-attention',
};

const NO_OP = () => {
  // Placeholder function meant to be overridden.
};

let UNDEFINED;

/**
 * FormExplainer
 * @class
 * @classdesc Initializes a new Form Explainer.
 * @param {HTMLElement} element - Base DOM element.
 * @param {object} options - Configuration options.
 * @returns {object} An Form Explainer instance.
 */
class FormExplainer {
  constructor(element, options = {}) {
    this.currentPage = options.currentPage || 1;
    this.elements = {};
  }

  /**
   * Initialize the FormExplainer.
   * @returns {FormExplainer} An instance.
   */
  init() {
    this.setPageCount();
    this.setCurrentPage(this.currentPage, UNDEFINED, false);
    this.setUIElements();
    this.initializeUI(this.elements);
    this.initializeEvents();

    return this;
  }

  /**
   * Initialize the UI after instatiation.
   * @param {object} elements - Current page DOM elements.
   */
  initializeUI(elements) {
    if (this.pageCount === 1) {
      DT.hide('.form-explainer__page-buttons');
    }

    DT.applyAll(elements.pages, (value, index) => {
      const _index = index + 1;
      if (_index > 1) {
        // Hide all but the first parge
        const _page = this.getPageEl(_index);
        DT.hide(_page);
      }
    });

    ExpandableGroup.init();
  }

  /**
   * Update the pagination UI.
   */
  updatePaginationUI() {
    const BTN_DISABLED = 'a-btn--disabled';
    const PAGE_BTN_CTR = '.form-explainer__page-buttons';

    if (this.pageCount > 1) {
      DT.removeClass(PAGE_BTN_CTR + ' button', BTN_DISABLED);
      if (this.currentPage === 1) {
        DT.addClass(PAGE_BTN_CTR + ' .prev', BTN_DISABLED);
      } else if (this.currentPage === this.pageCount) {
        DT.addClass(PAGE_BTN_CTR + ' .next', BTN_DISABLED);
      }
    }
  }

  /* Update attention classes based on the expandable or image overlay
   that was targeted.
   Remove the attention class from all the expandables/overlays,
   and then apply it to the target & its associated overlay
   or expandable.
   * @param {HTMLElement} target - Overlay or expandable DOM node.
   * @param {string} className - Hover class name.
   */
  updateAttention(target, className) {
    let associated;
    const targetId = target.getAttribute('id');

    DT.removeClass(
      '.o-expandable__form-explainer, .image-map__overlay',
      className,
    );

    if (target.getAttribute('href') !== null) {
      associated = DT.getEl(target.getAttribute('href'));
    } else if (targetId !== null) {
      associated = DT.getEl('[href="#' + targetId + '"]');
    }

    if (associated !== null) {
      if (className === CSS.HAS_ATTENTION) {
        DT.removeClass(target, CSS.HOVER_HAS_ATTENTION);
        DT.removeClass(associated, CSS.HOVER_HAS_ATTENTION);
      }
      DT.addClass(target, className);
      DT.addClass(associated, className);
    }
  }

  /**
   * Open the expandable and scroll into the viewport.
   * @param {HTMLElement} imageOverlay - Image overlay, which was clicked.
   * @param {HTMLElement} targetExpandable - Target expandable.
   * current focus.
   */
  openAndScrollToExpandable(imageOverlay, targetExpandable) {
    const targetExpandableTarget = targetExpandable.querySelector(
      '.o-expandable__header',
    );

    window.setTimeout(() => {
      scrollIntoView(targetExpandableTarget, {
        duration: 500,
        callback: () => targetExpandableTarget.focus(),
      });
    }, 150);
    window.setTimeout(() => targetExpandableTarget.click(), 0);
  }

  /**
   * Set the UI elements for the page
   * @returns {object} DOM elements for the page.
   */
  setUIElements() {
    const explain = DT.getEl('.explain');
    const explainPagination = explain.querySelector('.explain__pagination');
    const explainPageBtns = explain.querySelectorAll(
      '.form-explainer__page-buttons button',
    );
    const pages = explain.querySelectorAll('.explain__page');
    const formExplainerLinks = explain.querySelectorAll(
      '.form-explainer__page-link',
    );

    return Object.assign(this.elements, {
      explain,
      explainPageBtns,
      explainPagination,
      formExplainerLinks,
      pages,
    });
  }

  /**
   * Return explainer page element based on page number.
   * @param {number} pageNum - Number of explainer page.
   * @returns {object} Page DOM element.
   */
  getPageEl(pageNum) {
    return DT.getEl(`#explain__page-${pageNum}`);
  }

  /**
   * Paginate through the various form pages.
   * @param {string} direction - 'next' or 'prev'.
   */
  paginate(direction) {
    const currentPage = this.currentPage;
    const increment = direction === 'next' ? 1 : -1;
    const newPage = currentPage + increment;

    // Move to the next or previous page if it's not the first or last page.
    if (
      (direction === 'next' && newPage <= this.pageCount) ||
      (direction === 'prev' && newPage >= 1)
    ) {
      this.switchPage(currentPage, newPage);
    }
  }

  /**
   * Paginate through the various form pages.
   * @param {number} pageNum - Number of the current page.
   * @param {Function} callback - Function to invode after scroll.
   * @param {boolean} shouldScrollIntoView - Whether to scroll the page into view.
   */
  setCurrentPage(pageNum, callback, shouldScrollIntoView = true) {
    const CURRENT_PAGE = 'current-page';
    const PAGE_LINK = '.form-explainer__page-link';
    const PAGINATION = '.explain__pagination';
    const CURRENT_PAGE_LINK =
      '.form-explainer__page-link[data-page="' + pageNum + '"]';

    this.currentPage = parseInt(pageNum, 10);

    DT.removeClass(PAGE_LINK, CURRENT_PAGE);
    DT.addClass(CURRENT_PAGE_LINK, CURRENT_PAGE);
    this.updatePaginationUI();

    if (shouldScrollIntoView) {
      scrollIntoView(DT.getEl(PAGINATION), {
        duration: 200,
        callback: callback || NO_OP,
      });
    }
  }

  /**
   * Paginate through the various form pages.
   * @param {number} pageCount - Number of pages.
   */
  setPageCount(pageCount) {
    const pages = DT.getEls('.explain__page');
    this.pageCount = pageCount || pages.length;
  }

  /**
   * Switch pages by fading pages in / out and
   * updating the UI accordingly.
   * @param {number} currentPage - Current page Number.
   * @param {number} newPage - New page number.
   */
  switchPage(currentPage, newPage) {
    this.setCurrentPage(newPage, () => {
      // After scrolling the window, fade out the current page.
      DT.fadeOut(this.getPageEl(currentPage), 600, () => {
        DT.fadeIn(this.getPageEl(newPage), 700);
      });
    });
  }

  /* Initialize the DOM events for the entire explainer UI. */
  initializeEvents() {
    const uiElements = this.elements;

    if (this.pageCount > 1) {
      /* When a paginantion link is clicked,
       * switch to the next / previous page.
       */
      DT.bindEvents(uiElements.explainPageBtns, 'click', (event) => {
        const target = event.currentTarget;

        if (!DT.hasClass(target, 'disabled')) {
          const direction = DT.hasClass(target, 'prev') ? 'prev' : 'next';
          this.paginate(direction);
        }
      });

      /* When a page navigation link is clicked,
       * switch to the appropriate page.
       */
      DT.bindEvents(uiElements.formExplainerLinks, 'click', (event) => {
        const target = event.currentTarget;
        const pageNum = target.getAttribute('data-page');
        const currentPage = this.currentPage;

        if (!DT.hasClass(target, 'disabled') && pageNum !== currentPage) {
          this.switchPage(currentPage, pageNum);
        }
      });
    }

    /* When the mouse is over the image overlay or form explainer,
     * update the hover styles.
     */
    DT.bindEvents(
      '.image-map__overlay, .o-expandable__form-explainer',
      ['mouseenter', 'mouseleave'],
      (event) => {
        event.preventDefault();
        this.updateAttention(event.target, CSS.HOVER_HAS_ATTENTION);
      },
    );

    /* When a form explainer expandable target has the focus,
     * update the image overlay.
     */
    DT.bindEvents('.o-expandable__header', 'focus', (event) => {
      const expandable = event.target.closest('.o-expandable__form-explainer');
      this.updateAttention(expandable, CSS.HOVER_HAS_ATTENTION);
    });

    /* When an overlay is clicked, toggle the corresponding expandable
     * and scroll the page until it is in view.
     */
    DT.bindEvents('.image-map__overlay', 'click', (event) => {
      event.preventDefault();
      event.stopPropagation();
      const imageOverlay = event.target;
      const itemID = imageOverlay.getAttribute('href');
      const targetExpandable = DT.getEl(itemID);

      this.openAndScrollToExpandable(imageOverlay, targetExpandable);
    });

    /* When a form explainer expandable is clicked / pressed,
     * update the image overlay position and hover styles.
     */
    DT.bindEvents(
      '.o-expandable__form-explainer .o-expandable__header',
      ['click', 'keypress'],
      (event) => {
        if (event.which === 13 || event.type === 'click') {
          const closestFormExplainer = event.target.closest(
            '.o-expandable__form-explainer',
          );

          this.updateAttention(closestFormExplainer, CSS.HAS_ATTENTION);
        }
      },
    );
  }
}

export default FormExplainer;
