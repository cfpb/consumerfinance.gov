/* ==========================================================================
   Bureau structure.
   Scripts for `/the-bureau/bureau-structure/`.
   ========================================================================== */

import BreakpointHandler from '../modules/BreakpointHandler';
import Expandable from '@cfpb/cfpb-expandables/src/Expandable';

let BS;

const BureauStructure = BS = {

  elements: {},

  isMobile: false,

  vendorPrefixes: {},

  slideCount: 0,

  slideDuration: 0.35,

  slideIndex: 0,

  /**
   * Initializes the Breakpoint handler and sets the cached elements.
   */
  initialize: function initialize() {
    BS.setElements();
    BS.initializeExpandables();
    BS.slideCount = BS.elements.branches.length;

    new BreakpointHandler( {
      breakpoint: 600,
      type:       'max',
      enter:      BS.eventListeners.enterMobile,
      leave:      BS.eventListeners.leaveMobile
    } );
  },

  /**
   * Initialize the expandables and the expand/collapse event listeners.
   */
  initializeExpandables: function initializeExpandables() {
    const expandables = Expandable.init(
      document.querySelector( '.o-bureau-structure' )
    );

    let expandable;
    for ( const index in expandables ) {
      expandable = expandables[index];
      expandable.transition.addEventListener(
        'expandEnd', BS.eventListeners.heightChange
      );
      expandable.transition.addEventListener(
        'collapseEnd', BS.eventListeners.heightChange
      );
    }
  },

  /**
   * Remove the event listeners and destroy the slider navigation.
   */
  destroy: function destroy() {
    BS.elements.branch.removeAttribute( 'style' );
    for ( let i = BS.slideCount - 1; i >= 0; i-- ) {
      BS.elements.branches[i].removeAttribute( 'style' );
    }
    BS.removeEventListeners();
  },

  /**
   * Sets the cached elements.
   */
  setElements: function setElements() {
    const elements = BS.elements;
    elements.base = document.querySelector( '.o-bureau-structure_chart' );
    elements.branch =
      BS.elements.base.querySelector( '.o-bureau-structure_branches' );
    elements.branches =
      BS.elements.base.querySelectorAll( '.o-bureau-structure_branches > li' );
  },

  /**
   * Returns proper vendor prefix name
   * @param {string} style - css style.
   * @returns {object} vendor prefixes.
   */
  getVendorPrefix: function getVendorPrefix( style ) {
    const vendors = [ 'webkit', 'Moz', 'ms', 'O' ];
    const element = document.body;
    const existingPrefix = BS.vendorPrefixes[style] ||
                         element.style[style.toLowerCase()];

    if ( existingPrefix ) return existingPrefix;

    for ( let i = 0; i < vendors.length; i++ ) {
      if ( typeof element.style[vendors[i] + style] != 'undefined' ) {
        BS.vendorPrefixes[style] = vendors[i] + style;
        break;
      }
    }

    return BS.vendorPrefixes[style] || style;
  },

  /**
   * Get the slider width;
   * @returns {number} slider width.
   */
  getSliderWidth: function getSliderWidth() {
    return BS.elements.base.offsetWidth;
  },

  /**
   * Get the slider height;
   * @returns {number} slider height.
   */
  getSliderHeight: function getSliderHeight() {
    return BS.elements.branches[BS.slideIndex].offsetHeight + 'px';
  },

  /**
   * Sets the width on the necessary slider DOM elements.
   */
  setSliderWidth: function setSliderWidth() {
    BS.elements.branch.style.width =
      BS.getSliderWidth() * BS.slideCount + 'px';
    for ( let i = BS.slideCount - 1; i >= 0; i-- ) {
      BS.elements.branches[i].style.width = BS.getSliderWidth() + 'px';
    }
  },

  /**
   * Sets the height on the necessary slider DOM elements.
   */
  setSliderHeight: function() {
    BS.elements.branch.style.height = BS.getSliderHeight();
  },

  /**
   * Move the current / next slide using prefixed CSS properties.
   * @param {number} slideIndex - zero based index of the slide.
   */
  moveSlide: function moveSlide( slideIndex ) {
    const branches = BS.elements.branches;
    const sign = slideIndex > BS.slideIndex ? '-' : '';
    const index = Array.prototype.indexOf.call( branches, branches[slideIndex] );
    const transForm = 'translate(' + sign + 100 * index + '%, 0)';
    const prefixedTransitionDuration = BS.getVendorPrefix( 'TransitionDuration' );
    const prefixedTransform = BS.getVendorPrefix( 'Transform' );
    const nextSlideStyle = branches[slideIndex].style;

    if ( slideIndex > BS.slideIndex ) {
      nextSlideStyle[prefixedTransitionDuration] = '0s';
      nextSlideStyle[prefixedTransform] =
        'translate(-' + 100 * ( index - 1 ) + '%, 0)';
    }

    nextSlideStyle[prefixedTransitionDuration] = BS.slideDuration + 's';
    branches[BS.slideIndex].style[prefixedTransform] = transForm;
    nextSlideStyle[prefixedTransform] = transForm;

    BS.slideIndex = slideIndex;
    BS.setSliderHeight();
  },

  /**
   * Add the event listeners for window resize and navigation click.
   */
  addEventListeners: function addEventListeners() {
    window.addEventListener( 'resize', BS.eventListeners.resize );
    BS.elements.branch.addEventListener( 'click', BS.eventListeners.navClick );
  },

  /**
   * Remove the event listeners from the slider navigation.
   */
  removeEventListeners: function removeEventListeners() {
    window.removeEventListener( 'resize', BS.eventListeners.resize );
    BS.elements.branch.removeEventListener(
      'click', BS.eventListeners.navClick
    );
  },

  eventListeners: {

    /**
     * Event handler called when entering the mobile Breakpoint.
     */
    enterMobile: function enterMobile() {
      BS.slideIndex = 0;
      BS.isMobile = true;
      BS.addEventListeners();
      BS.setSliderWidth();
      BS.setSliderHeight();
    },

    /**
     * Event handler called when leaving the mobile Breakpoint.
     */
    leaveMobile: function leaveMobile() {
      BS.isMobile = false;
      BS.destroy();
    },

    /**
     * Event handler called when height of the Bureau Structure changes.
     */
    heightChange: function heightChange() {
      if ( BS.isMobile === false ) return;
      BS.setSliderHeight();
    },

    /**
     * Event handler called when the navigation is clicked.
     * @param {Object} event - Browser click event.
     */
    navClick: function navClick( event ) {
      const slideIndex = event.target.getAttribute( 'data-show-slide-index' );
      if ( slideIndex ) {
        BS.moveSlide( slideIndex );
      }
    },

    /**
     * Event handler called when the window is resized.
     */
    resize: function resize() {
      BS.setSliderWidth();
    }
  }
};

export default BureauStructure;
