/* ==========================================================================
   Bureau structure.
   Scripts for `/the-bureau/bureau-structure/`.
   ========================================================================== */

'use strict';

var BreakpointHandler = require( './BreakpointHandler' );
var Expandable = require( '../organisms/Expandable' );
var UNDEFINED;
var BS;

var BureauStructure = BS = {

  elements: {},

  expandables: [],

  vendorPrefix: UNDEFINED,

  slideCount: 0,

  slideDuration: 0.35,

  slideIndex: 0,

  /**
   * Initializes the Breakpoint handler and sets the cached elements.
   */
  initialize: function initialize() {
    BS.setElements();
    BS.vendorPrefix = BS.getVendorPrefix();
    BS.slideCount = BS.elements.branches.length;

    new BreakpointHandler( {
      breakpoint: 600,
      type:       'max',
      enter:      BS.eventListeners.enterMobile,
      leave:      BS.eventListeners.leaveMobile
    } );
  },

  /**
   * Remove the event listeners and destroy the expandables.
   */
  destroy: function destroy() {
    BS.elements.branch.removeAttribute( 'style' );
    for ( var i = BS.slideCount - 1; i >= 0; i-- ) {
      BS.elements.branches[i].removeAttribute( 'style' );
    }
    BS.removeEventListeners();
    BS.destroyExpandables();
  },

  /**
   * Sets the cached elements.
   */
  setElements: function setElements() {
    var elements = BS.elements;
    elements.base = document.querySelector( '.org-chart' );
    elements.branch = BS.elements.base.querySelector( '.org-chart_branches' );
    elements.branches =
      BS.elements.base.querySelectorAll( '.org-chart_branches > li' );
  },

  /**
   * Returns proper vendor prefix name
   * Code copied from https://davidwalsh.name/vendor-prefix.
   * @returns {object} vendor prefixes.
  */
  getVendorPrefix: function getVendorPrefix() {
    var ua = navigator.userAgent.toLowerCase();
    var match = /opera/.exec( ua ) ||
                /msie/.exec( ua ) ||
                /firefox/.exec( ua ) ||
                /(chrome|safari)/.exec( ua ) ||
                []; // eslint-disable-line  wrap-regex, inline-comments, max-len

    var vendors = {
      opera: 'O',
      chrome: 'webkit',
      safari: 'webkit',
      firefox: 'Moz',
      msie: 'ms'
    };

    return vendors[match[0]];
  },

  /**
   * Initialize the expandables and the expand / collapse event listeners.
   */
  initializeExpandables: function initializeExpandables() {
    // Initialize the Expandable.
    var expandablesDom = document.querySelectorAll( '.o-expandable' );
    var expandable;
    for ( var i = 0, len = expandablesDom.length; i < len; i++ ) {
      expandable = new Expandable( expandablesDom[i] );
      // Ensure Expandable isn't coming from cloned DOM nodes.
      expandable.destroy();
      expandable.addEventListener( 'expandEnd',
        BS.eventListeners.heightChange );
      expandable.addEventListener( 'collapseEnd',
        BS.eventListeners.heightChange );
      expandable.init();
      BS.expandables.push( expandable );
    }
  },

  /**
   * Remove the event listeners from the expandables and destroy the
   * Expandables instances.
   */
  destroyExpandables: function destroyExpandables() {
    for ( var i = 0, len = BS.expandables.length; i < len; i++ ) {
      BS.expandables[i].removeEventListener( 'expandEnd',
        BS.eventListeners.heightChange );
      BS.expandables[i].removeEventListener( 'collapseEnd',
        BS.eventListeners.heightChange );
      BS.expandables[i].destroy();
    }
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
    for ( var i = BS.slideCount - 1; i >= 0; i-- ) {
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
    var branches = BS.elements.branches;
    var sign = slideIndex > BS.slideIndex ? '-' : '';
    var index = Array.prototype.indexOf.call( branches, branches[slideIndex] );
    var transForm = 'translate(' + sign + 100 * index + '%, 0)';
    var prefixedTransitionDuration = BS.vendorPrefix + 'TransitionDuration';
    var prefixedTransform = BS.vendorPrefix + 'Transform';
    var nextSlideStyle = branches[slideIndex].style;

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
   * Remove the event listeners from the expandables and the slider navigation.
   */
  removeEventListeners: function removeEventListeners() {
    window.removeEventListener( 'resize', BS.eventListeners.resize );
    BS.elements.branch.removeEventListener( 'click',
      BS.eventListeners.navClick );
  },

  eventListeners: {

    /**
     * Event handler called when entering the mobile Breakpoint.
     */
    enterMobile: function enterMobile() {
      BS.slideIndex = 0;
      BS.initializeExpandables();
      BS.addEventListeners();
      BS.setSliderWidth();
      BS.setSliderHeight();
    },

    /**
     * Event handler called when leaving the mobile Breakpoint.
     */
    leaveMobile: function leaveMobile() {
      BS.destroy();
    },

    /**
     * Event handler called when height of the Bureau Structure changes.
     */
    heightChange: function heightChange() {
      BS.setSliderHeight();
    },

    /**
     * Event handler called when the navigation is clicked.
     * @param {Object} event - Browser click event.
     */
    navClick: function navClick( event ) {
      var slideIndex = event.target.getAttribute( 'data-show-slide-index' );
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

module.exports = BureauStructure;
