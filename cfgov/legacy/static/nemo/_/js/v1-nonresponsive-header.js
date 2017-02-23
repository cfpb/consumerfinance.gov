/**
 * Generated via Gulp in https://github.com/cfpb/cfgov-refresh/
 * On March 29, 2016
 *
 * To Reproduce:
 * - Edit webpack-config.js to remove banner and un-uglify
 * - Remove everything but header.js and focus-target in main.js
 * - Edit any functions that check for breakpoints like `isInDesktop` to return desktop only JS
 * - Run gulp and paste below.
 *
 * To use in project: Run grunt header to minify
**/



/******/ (function(modules) { // webpackBootstrap
/******/  // install a JSONP callback for chunk loading
/******/  var parentJsonpFunction = window["webpackJsonp"];
/******/  window["webpackJsonp"] = function webpackJsonpCallback(chunkIds, moreModules) {
/******/    // add "moreModules" to the modules object,
/******/    // then flag all "chunkIds" as loaded and fire callback
/******/    var moduleId, chunkId, i = 0, callbacks = [];
/******/    for(;i < chunkIds.length; i++) {
/******/      chunkId = chunkIds[i];
/******/      if(installedChunks[chunkId])
/******/        callbacks.push.apply(callbacks, installedChunks[chunkId]);
/******/      installedChunks[chunkId] = 0;
/******/    }
/******/    for(moduleId in moreModules) {
/******/      modules[moduleId] = moreModules[moduleId];
/******/    }
/******/    if(parentJsonpFunction) parentJsonpFunction(chunkIds, moreModules);
/******/    while(callbacks.length)
/******/      callbacks.shift().call(null, __webpack_require__);
/******/    if(moreModules[0]) {
/******/      installedModules[0] = 0;
/******/      return __webpack_require__(0);
/******/    }
/******/  };

/******/  // The module cache
/******/  var installedModules = {};

/******/  // object to store loaded and loading chunks
/******/  // "0" means "already loaded"
/******/  // Array means "loading", array contains callbacks
/******/  var installedChunks = {
/******/    3:0
/******/  };

/******/  // The require function
/******/  function __webpack_require__(moduleId) {

/******/    // Check if module is in cache
/******/    if(installedModules[moduleId])
/******/      return installedModules[moduleId].exports;

/******/    // Create a new module (and put it into the cache)
/******/    var module = installedModules[moduleId] = {
/******/      exports: {},
/******/      id: moduleId,
/******/      loaded: false
/******/    };

/******/    // Execute the module function
/******/    modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);

/******/    // Flag the module as loaded
/******/    module.loaded = true;

/******/    // Return the exports of the module
/******/    return module.exports;
/******/  }

/******/  // This file contains only the entry chunk.
/******/  // The chunk loading function for additional chunks
/******/  __webpack_require__.e = function requireEnsure(chunkId, callback) {
/******/    // "0" is the signal for "already loaded"
/******/    if(installedChunks[chunkId] === 0)
/******/      return callback.call(null, __webpack_require__);

/******/    // an array means "currently loading".
/******/    if(installedChunks[chunkId] !== undefined) {
/******/      installedChunks[chunkId].push(callback);
/******/    } else {
/******/      // start chunk loading
/******/      installedChunks[chunkId] = [callback];
/******/      var head = document.getElementsByTagName('head')[0];
/******/      var script = document.createElement('script');
/******/      script.type = 'text/javascript';
/******/      script.charset = 'utf-8';
/******/      script.async = true;

/******/      script.src = __webpack_require__.p + "" + chunkId + "." + ({"0":"browse-filterable/index.js","1":"careers/current-openings/index.js","2":"careers/working-at-cfpb/index.js","4":"external-site/index.js","5":"on-demand/expandable-group.js","6":"on-demand/expandable.js","7":"on-demand/filterable-list-controls.js","8":"on-demand/notification.js","9":"on-demand/secondary-navigation.js","10":"sheer.js","11":"the-bureau/bureau-structure/index.js","12":"the-bureau/index.js"}[chunkId]||chunkId) + "";
/******/      head.appendChild(script);
/******/    }
/******/  };

/******/  // expose the modules object (__webpack_modules__)
/******/  __webpack_require__.m = modules;

/******/  // expose the module cache
/******/  __webpack_require__.c = installedModules;

/******/  // __webpack_public_path__
/******/  __webpack_require__.p = "";

/******/  // Load entry module and return exports
/******/  return __webpack_require__(0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ function(module, exports, __webpack_require__) {

  /* ==========================================================================
     Common application-wide scripts that are used across the whole site.
     ========================================================================== */

  'use strict';


  __webpack_require__( 19 ).init();

  // GLOBAL ATOMIC ELEMENTS.
  // Organisms.
  var Header = __webpack_require__( 20 );
  var header = new Header( document.body );
  // Initialize header by passing it reference to global overlay atom.
  header.init( document.body.querySelector( '.a-overlay' ) );


/***/ },
/* 1 */,
/* 2 */
/***/ function(module, exports) {

  /* ==========================================================================
     Atomic Helpers.

     Utilities for helping validate atomic design element architecture.
     ========================================================================= */

  'use strict';

  // TODO: Update baseClass to baseSel to handle CSS selector instead of a class.
  /**
   * @param {HTMLNode} element
   *   The DOM element within which to search for the atomic element class.
   * @param {string} baseClass The CSS class name for the atomic element.
   * @param {string} atomicName
   *   The name of the atomic element in CapitalizedCamelCase.
   * @returns {HTMLNode} The DOM element for the atomic element.
   * @throws {Error} If DOM element passed into the atomic element is not valid.
   */
  function checkDom( element, baseClass, atomicName ) {
    var msg;
    var dom;
    if ( !element || !element.classList ) {
      msg = element + ' passed to ' + atomicName + '.js is not valid. ' +
            'Check that element is a valid DOM node';
      throw new Error( msg );
    }

    dom = element.classList.contains( baseClass ) ?
          element : element.querySelector( '.' + baseClass );

    if ( !dom ) {
      msg = baseClass + ' not found on or in passed DOM node.';
      throw new Error( msg );
    }

    return dom;
  }

  // Expose public methods.
  module.exports = {
    checkDom: checkDom
  };


/***/ },
/* 3 */
/***/ function(module, exports, __webpack_require__) {

  'use strict';

  // Required modules.
  var atomicHelpers = __webpack_require__( 2 );
  var breakpointState = __webpack_require__( 4 );
  var EventObserver = __webpack_require__( 7 );

  /**
   * Expandable
   * @class
   *
   * @classdesc Initializes a new Expandable molecule.
   *
   * @param {HTMLNode} element
   *   The DOM element within which to search for the molecule.
   * @returns {Object} An Expandable instance.
   */
  function Expandable( element ) { // eslint-disable-line max-statements, inline-comments, max-len

    var BASE_CLASS = 'm-expandable';

    // Bitwise flags for the state of this Expandable.
    var COLLAPSED = 0;
    var COLLAPSING = 1;
    var EXPANDING = 2;
    var EXPANDED = 3;

    // The Expandable element will directly be the Expandable
    // when used in an ExpandableGroup, otherwise it can be the parent container.
    var _dom = atomicHelpers.checkDom( element, BASE_CLASS, 'Expandable' );
    var _target = _dom.querySelector( '.' + BASE_CLASS + '_target' );
    var _content = _dom.querySelector( '.' + BASE_CLASS + '_content' );
    var _contentAnimated =
      _content.querySelector( '.' + BASE_CLASS + '_content-animated' );
    var _link = _dom.querySelector( '.' + BASE_CLASS + '_link' );

    var _state = COLLAPSED;
    var _transitionEndEvent = _getTransitionEndEvent( _content );
    var _contentHeight;

    // TODO: Replace function of _that with Function.prototype.bind.
    var _that = this;
    var _collapseBinded = collapse.bind( this );
    var _expandBinded = expand.bind( this );

    /**
     * @param {number} state
     *   Allows passing of EXPANDED flag to set expanded state.
     * @returns {Object} The Expandable instance.
     */
    function init( state ) {
      _calcHeight();
      // Even if expanded is set, don't expand if in mobile window size.
      if ( !_isInMobile() &&
           ( state === EXPANDED ||
           _dom.getAttribute( 'data-state' ) === 'expanded' ) ) {
        // If expanded by default, we need to set the height inline so the
        // inline transition to collapse the Expandable works.
        // TODO: Handle issue of height calculating before
        //       web fonts have loaded and changed height.
        _setMaxHeight();
        _setExpandedState();
      } else {
        _setCollapsedState();
      }

      // Show the show/hide links, which otherwise are hidden if JS is off.
      _link.classList.remove( 'u-hidden' );

      _target.addEventListener( 'click', _handleClick );

      window.addEventListener( 'resize', _resizeHandler );

      _initObserver();

      return this;
    }

    /**
     * Watch for the insertion/removal of DOM nodes.
     * @returns {Object} The Expandable instance.
     */
    function _initObserver() {
      var MutationObserver = window.MutationObserver ||
                             window.WebKitMutationObserver ||
                             window.MozMutationObserver;
      var observeDOM;

      if ( MutationObserver ) {
        observeDOM = function() {
          var observer = new MutationObserver( function( mutations ) {
            mutations.forEach( _refreshHeight );
          } );

          observer.observe( _content, { childList: true, subtree: true } );
        };
      } else {
        observeDOM = function() {
          _content.addEventListener( 'DOMNodeInserted', _refreshHeight, false );
          _content.addEventListener( 'DOMNodeRemoved', _refreshHeight, false );
        };
      }

      window.setTimeout( observeDOM, 0 );

      return _that;
    }

    /**
     * @param {number} duration
     *   The duration of the sliding animation in milliseconds.
     * @returns {Object} The Expandable instance.
     */
    function toggle( duration ) {
      if ( _isExpanded() ) {
        _collapseBinded( duration );
      } else {
        _expandBinded( duration );
      }
      return _that;
    }

    /**
     * @param {number} duration
     *   The duration of the sliding animation in milliseconds.
     * @returns {Object} The Expandable instance.
     */
    function expand( duration ) {
      if ( _isExpanded() || _isExpanding() ) {
        return this;
      }

      duration = duration || _calculateExpandDuration( _contentHeight );

      _setStateTo( EXPANDING );
      this.dispatchEvent( 'beginExpand', { target: _that } );
      _setMaxHeight();
      _transitionHeight( _expandComplete, duration );
      return this;
    }

    /**
     * @param {number} duration
     *   The duration of the sliding animation in milliseconds.
     * @returns {Object} The Expandable instance.
     */
    function collapse( duration ) {
      if ( _isCollapsed() || _isCollapsing() ) {
        return this;
      }

      duration = duration || _calculateCollapseDuration( _contentHeight );

      _setStateTo( COLLAPSING );
      this.dispatchEvent( 'beginCollapse', { target: _that } );
      _setMinHeight();
      _transitionHeight( _collapseComplete, duration );
      return this;
    }

    /**
     * Transition height property and call a callback function.
     * Call callback directly if CSS transitions aren't supported.
     * @param {Function} callback Callback function for completion of transition.
     * @param {number} duration
     *   The duration of the sliding animation in milliseconds.
     */
    function _transitionHeight( callback, duration ) {
      if ( _transitionEndEvent ) {
        _content.addEventListener( _transitionEndEvent, callback );
        _content.style.transition = 'height ' + duration + 's ease-out';
      } else {
        // TODO: Remove callback-return ESLint ignore
        callback(); // eslint-disable-line callback-return, inline-comments, max-len
      }
    }

    /**
     * Configure the expanded state appearance.
     */
    function _setExpandedState() {
      _dom.classList.add( BASE_CLASS + '__expanded' );
      _content.setAttribute( 'aria-expanded', 'true' );
      _target.setAttribute( 'aria-pressed', 'true' );
      _setStateTo( EXPANDED );
    }

    /**
     * Configure the collapsed state appearance.
     */
    function _setCollapsedState() {
      _dom.classList.remove( BASE_CLASS + '__expanded' );
      _content.setAttribute( 'aria-expanded', 'false' );
      _target.setAttribute( 'aria-pressed', 'false' );
      _setStateTo( COLLAPSED );
    }

    /**
     * Expand animation has completed.
     */
    function _expandComplete() {
      _content.removeEventListener( _transitionEndEvent, _expandComplete );
      _setExpandedState();
      _that.dispatchEvent( 'endExpand', { target: _that } );
    }

    /**
     * Collapse animation has completed.
     */
    function _collapseComplete() {
      _content.removeEventListener( _transitionEndEvent, _collapseComplete );
      _setCollapsedState();
      _that.dispatchEvent( 'endCollapse', { target: _that } );
    }

    /**
     * Handle click of the Expandable target.
     */
    function _handleClick() {
      // Bubble click event outside of the Expandable.
      _that.dispatchEvent( 'click', { target: _that } );
      if ( _isCollapsed() || _isExpanded() ) {
        _that.toggle();
      }
    }

    /**
     * Refresh calculated height of content area.
     */
    function _calcHeight() {
      _contentHeight = _contentAnimated.offsetHeight;
    }

    /**
     * Handle a resize of the window.
     */
    function _resizeHandler() {
      _refreshHeight();
      if ( _isInMobile() ) {
        _collapseBinded();
      }
    }

    /**
     * Reset the height of the Expandables, when e.g. resizing the window.
     */
    function _refreshHeight() {
      if ( _isExpanded() ) {
        _setMaxHeight();
      } else {
        _setMinHeight();
      }
    }

    /**
     * Calculate and set the height based on the contents' height.
     */
    function _setMaxHeight() {
      _calcHeight();
      _content.style.height = _contentHeight + 'px';
    }

    /**
     * Set the height to zero.
     */
    function _setMinHeight() {
      _content.style.height = '0';
    }

    /**
     * @returns {boolean} Whether Expandable is in a collapsed state.
     */
    function _isCollapsed() {
      return _state === COLLAPSED;
    }

    /**
     * @returns {boolean} Whether Expandable is collapsing.
     */
    function _isCollapsing() {
      return _state === COLLAPSING;
    }

    /**
     * @returns {boolean} Whether Expandable is expanding.
     */
    function _isExpanding() {
      return _state === EXPANDING;
    }

    /**
     * @returns {boolean} Whether Expandable is in a expanded state.
     */
    function _isExpanded() {
      return _state === EXPANDED;
    }

    /**
     * @param {number} state Set the hide/show state flag for the Expandable.
     * @returns {number} Whether Expandable is in a expanded state.
     */
    function _setStateTo( state ) {
      _state = state;
      return _state;
    }

    // TODO: Move this to breakpoint-state.js.
    /**
     * Whether currently in the desktop view.
     * @returns {boolean} True if in the desktop view, otherwise false.
     */
    function _isInMobile() {
      return false;
    }

    // Attach public events.
    var eventObserver = new EventObserver();
    this.addEventListener = eventObserver.addEventListener;
    this.removeEventListener = eventObserver.removeEventListener;
    this.dispatchEvent = eventObserver.dispatchEvent;

    this.init = init;
    this.toggle = toggle;
    this.expand = expand;
    this.collapse = collapse;

    // Export constants so initialization signature can support, e.g.
    // var item = new Expandable( '.item' );
    // item.init( item.EXPANDED );
    // TODO: Move these to Expandable.COLLAPSED and Expandable.EXPANDED.
    //       So that they are set on the constructor, not an instance.
    this.COLLAPSED = COLLAPSED;
    this.EXPANDED = EXPANDED;

    return this;
  }

  // TODO: Use MoveTransition so this can be removed.
  /**
   * @param {HTMLNode} elm
   *   The element to check for support of transition end event.
   * @returns {string} The browser-prefixed transition end event.
   */
  function _getTransitionEndEvent( elm ) {
    var transition;
    var transitions = {
      WebkitTransition: 'webkitTransitionEnd',
      MozTransition:    'transitionend',
      OTransition:      'oTransitionEnd otransitionend',
      transition:       'transitionend'
    };

    for ( var t in transitions ) {
      if ( transitions.hasOwnProperty( t ) &&
           typeof elm.style[t] !== 'undefined' ) {
        transition = transitions[t];
        break;
      }
    }
    return transition;
  }

  /**
   * @param {number} height The height of the expandable content area in pixels.
   * @returns {number} The amount of time over which to expand in seconds.
   */
  function _calculateExpandDuration( height ) {
    return _constrainValue( 225, 450, height ) / 1000;
  }

  /**
   * @param {number} height The height of the expandable content area in pixels.
   * @returns {number} The amount of time over which to expand in seconds.
   */
  function _calculateCollapseDuration( height ) {
    return _constrainValue( 175, 450, height / 2 ) / 1000;
  }

  /**
   * @param {number} min The minimum height in pixels.
   * @param {number} max The maximum height in pixels.
   * @param {number} duration
   *   The amount of time over which to expand in milliseconds.
   * @returns {number} The amount of time over which to expand in milliseconds,
   *   constrained to within the min/max values.
   */
  function _constrainValue( min, max, duration ) {
    if ( duration > max ) {
      return max;
    } else if ( duration < min ) {
      return min;
    }
    return duration;
  }

  module.exports = Expandable;


/***/ },
/* 4 */
/***/ function(module, exports, __webpack_require__) {

  /* ==========================================================================
     Get Breakpoint State
     ========================================================================== */

  'use strict';

  var _breakpointsConfig = __webpack_require__( 5 );
  var _getViewportDimensions = __webpack_require__( 6 )
                               .getViewportDimensions;

  /**
   * @param {Object} breakpointRange - Object containing breakpoint constants.
   * @param {integer} width - Current window width.
   * @returns {boolean} Whether the passed width is within a breakpoint range.
   */
  function _inBreakpointRange( breakpointRange, width ) {
    var min = breakpointRange.min || 0;
    var max = breakpointRange.max || Number.POSITIVE_INFINITY;

    return min <= width && width <= max;
  }

  /**
   * @param {integer} width - Current window width.
   * @returns {Object} An object literal with boolean
   *   isBpXS, isBpSM, isBpMED, isBpLG, isBpXL properties.
   */
  function get( width ) {
    var breakpointState = {};
    var breakpointKey;
    width = width || _getViewportDimensions().width;

    for ( var rangeKey in _breakpointsConfig ) { // eslint-disable-line guard-for-in, no-inline-comments, max-len
      breakpointKey = 'is' + rangeKey.charAt( 0 ).toUpperCase() +
                      rangeKey.slice( 1 );
      breakpointState[breakpointKey] =
        _inBreakpointRange( _breakpointsConfig[rangeKey], width );
    }

    return breakpointState;
  }

  // Expose public methods.
  module.exports = { get: get };


/***/ },
/* 5 */
/***/ function(module, exports) {

  'use strict';

  // TODO: Read these values directly from cf-vars.less.
  // All values are pixel based.

  module.exports = {
    bpXS: {
      min: 0,
      max: 600
    },
    bpSM: {
      min: 601,
      max: 900
    },
    bpMED: {
      min: 901,
      max: 1020
    },
    bpLG: {
      min: 1021,
      max: 1200
    },
    bpXL: {
      min: 1201
    }
  };


/***/ },
/* 6 */
/***/ function(module, exports) {

  /* ==========================================================================
     Get Viewport Dimensions
     ========================================================================== */

  'use strict';

  /**
   * @returns {object} An object literal with the viewport
   *   width and height as properties.
   */
  function getViewportDimensions() {
    // TODO: Check what browsers this is necessary for and
    // check whether it is still applicable.
    var viewportEl = window;
    var propPrefix = 'inner';
    var modernBrowser = 'innerWidth' in window;
    if ( !modernBrowser ) {
      viewportEl = document.documentElement || document.body;
      propPrefix = 'client';
    }

    return {
      width:  viewportEl[propPrefix + 'Width'],
      height: viewportEl[propPrefix + 'Height']
    };
  }

  // Expose public methods.
  module.exports = {
    getViewportDimensions: getViewportDimensions
  };


/***/ },
/* 7 */
/***/ function(module, exports) {

  'use strict';

  /**
   * EventObserver
   * @class
   *
   * @classdesc Used for creating an object
   *   that can be used to dispatch and listen to custom events.
   * @returns {Object} An EventObserver instance.
   */
  function EventObserver() {

    // The events registered on this instance.
    var _events = {};

    /**
     * Register an event listener.
     * @param {string} event - The event name to listen for.
     * @param {Function} callback - The function called when the event has fired.
     * @returns {Object} The instance this EventObserver instance is decorating.
     */
    function addEventListener( event, callback ) {
      if ( _events.hasOwnProperty( event ) ) {
        _events[event].push( callback );
      } else {
        _events[event] = [ callback ];
      }

      return this;
    }

    /**
     * Remove an added event listener.
     * Must match a call made to addEventListener.
     * @param {string} event - The event name to remove.
     * @param {Function} callback - The function attached to the event.
     * @returns {Object} The instance this EventObserver instance is decorating.
     */
    function removeEventListener( event, callback ) {
      if ( !_events.hasOwnProperty( event ) ) {
        return this;
      }

      var index = _events[event].indexOf( callback );
      if ( index !== -1 ) {
        _events[event].splice( index, 1 );
      }

      return this;
    }

    /**
     * Broadcast an event.
     * @param {string} event - The type of event to broadcast.
     * @param {Object} options - The event object to pass to the event handler.
     * @returns {Object} The instance this EventObserver instance is decorating.
     */
    function dispatchEvent( event, options ) {
      if ( !_events.hasOwnProperty( event ) ) {
        return this;
      }

      options = options || {};

      var evts = _events[event];
      for ( var i = 0, len = evts.length; i < len; i++ ) {
        evts[i].call( this, options );
      }

      return this;
    }

    EventObserver.prototype.addEventListener = addEventListener;
    EventObserver.prototype.removeEventListener = removeEventListener;
    EventObserver.prototype.dispatchEvent = dispatchEvent;

    return this;
  }

  module.exports = EventObserver;


/***/ },
/* 8 */,
/* 9 */,
/* 10 */,
/* 11 */,
/* 12 */,
/* 13 */,
/* 14 */,
/* 15 */,
/* 16 */
/***/ function(module, exports) {

  module.exports = jQuery;

/***/ },
/* 17 */,
/* 18 */,
/* 19 */
/***/ function(module, exports, __webpack_require__) {

  /* ==========================================================================
     Focus Target

     This is necessary because of a webkit quirk with handling keyboard
     focus with anchor links. It'll mostly be used on the skip nav link.

     If that webkit bug is fixed, remove this JS.

  ========================================================================== */

  'use strict';

  var $ = __webpack_require__( 16 );

  /**
   * Parse links to handle webkit bug with keyboard focus.
   */
  function init() {
    $( 'a[href^="#"]' ).click( function() {
      var anchor = $( this ).attr( 'href' );
      $( anchor ).attr( 'tabindex', -1 ).focus();
    } );
  }

  module.exports = { init: init };


/***/ },
/* 20 */
/***/ function(module, exports, __webpack_require__) {

  'use strict';

  // Required modules.
  var atomicHelpers = __webpack_require__( 2 );
  var GlobalBanner = __webpack_require__( 21 );
  var GlobalSearch = __webpack_require__( 23 );
  var MegaMenu = __webpack_require__( 30 );

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

    var BASE_CLASS = 'o-header';

    var _dom = atomicHelpers.checkDom( element, BASE_CLASS, 'Header' );

    var _globalbanner;
    var _globalSearch;
    var _megaMenu;
    var _overlay;

    /**
     * @param {HTMLNode} overlay
     *   Overlay to show/hide when mobile mega menu is shown.
     * @returns {Object} The Header instance.
     */
    function init( overlay ) {
      // TODO: Investigate a better method of handling optional elements.
      //       Banner is optional, so we don't want to throw a nice error
      //       when its DOM isn't found.
      try {
        _globalbanner = new GlobalBanner( _dom );
        _globalbanner.init();
      } catch( err ) {
        // No Banner to initialize.
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

  module.exports = Header;


/***/ },
/* 21 */
/***/ function(module, exports, __webpack_require__) {

  /* ==========================================================================
     Collapsing Global banner.
     Remember banner state (collapsed or open) across sessions.
     ========================================================================== */

  'use strict';

  // Required modules.
  var atomicHelpers = __webpack_require__( 2 );
  var Expandable = __webpack_require__( 3 );
  var webStorageProxy = __webpack_require__( 22 );

  /**
   * GlobalBanner
   * @class
   *
   * @classdesc Initializes a new GlobalBanner molecule.
   *
   * @param {HTMLNode} element
   *   The DOM element within which to search for the molecule.
   * @returns {GlobalBanner} An instance.
   */
  function GlobalBanner( element ) {

    var BASE_CLASS = 'm-global-banner';
    var EXPANDED_STATE = 'globalBannerIsExpanded';

    var _dom = atomicHelpers.checkDom( element, BASE_CLASS, 'GlobalBanner' );
    var _expandable;

    /**
     * Set up DOM references and event handlers.
     */
    function init() {
      // Init Expandable.
      var isExpanded = webStorageProxy.getItem( EXPANDED_STATE ) !== 'false';
      _expandable = new Expandable( _dom.querySelector( '.m-expandable' ) );
      _expandable.init( isExpanded && _expandable.EXPANDED );

      _initEvents();
    }

    /**
     * Run when the beta in-progress banner has been clicked.
     */
    function _initEvents() {
      _expandable.addEventListener( 'click', toggleStoredState );
    }

    /**
     * Remove event handlers and local storage data.
     */
    function destroy() {
      _expandable.removeEventListener( 'click', toggleStoredState );
      webStorageProxy.removeItem( EXPANDED_STATE, true );
    }

    /**
     * Toggle the boolean value stored in a web storage.
     * @returns {boolean} Returns value stored in the web storage,
     * either true or false.
     */
    function toggleStoredState() {
      var value = webStorageProxy.getItem( EXPANDED_STATE );

      if ( value === 'false' ) {
        webStorageProxy.setItem( EXPANDED_STATE, true );
      } else {
        webStorageProxy.setItem( EXPANDED_STATE, false );
      }
      return value;
    }

    this.init = init;
    this.destroy = destroy;
    this.toggleStoredState = toggleStoredState;

    return this;
  }

  // Expose public methods.
  module.exports = GlobalBanner;


/***/ },
/* 22 */
/***/ function(module, exports) {

  /* ==========================================================================
     Web Storage proxy utility.

     An interface for interacting with web storage
     (local storage and session storage).
     Note: values stored in local storage are not accessible from session storage
     and vice versa. They both work on different objects within the browser.
     If web storage is not available, values are dumped into an object literal
     to keep the fuctionality of the API, but will not be saved across sessions.
     ========================================================================= */

  'use strict';

  // Default storage type.
  var _storage;

  /**
   * Set an item value specified by the key in web storage.
   * @param {string} key The key for the value.
   * @param {string} value The value to store.
   * @param {Object} storage (Optional)
   *   Use non-persistent storage (sessionStorage)
   *   or persistent storage (localStorage).
   * @returns {string} The value set in web storage.
   */
  function setItem( key, value, storage ) {
    storage = _getStorageType( storage );
    if ( storage.setItem ) {
      storage.setItem( key, value );
    } else {
      storage[key] = value;
    }

    return value;
  }

  /**
   * Get an item value specified by the key in web storage.
   * @param {string} key The key for the value.
   * @param {Object} storage (Optional)
   *   Use non-persistent storage (sessionStorage)
   *   or persistent storage (localStorage).
   * @returns {string} The value set in web storage.
   */
  function getItem( key, storage ) {
    storage = _getStorageType( storage );

    return storage.getItem ? storage.getItem( key ) : storage[key];
  }

  /**
   * Remove an item specified by the key.
   * @param {string} key The key for the value.
   * @param {Object} storage (Optional)
   *   Use non-persistent storage (sessionStorage)
   *   or persistent storage (localStorage).
   * @returns {boolean} Returns true if the item existed and it was
   *   removed. Returns false if the item didn't exist to begin with.
   */
  function removeItem( key, storage ) {
    storage = _getStorageType( storage );
    var returnVal = true;

    if ( !getItem( key, storage ) ) {
      returnVal = false;
    }

    if ( returnVal ) {
      if ( storage.removeItem ) {
        storage.removeItem( key );
      } else {
        delete storage[key];
      }
    }

    return returnVal;
  }

  /**
   * Set the default session type.
   * @param {object} storage
   *   Use non-persistent storage (sessionStorage)
   *   or persistent storage (localStorage).
   * @throws {Error} If parameter isn't a object.
   */
  function setStorage( storage ) {
    if ( typeof storage !== 'object' ) {
      throw new Error( 'Setting must be an object.' );
    }

    _storage = storage;
  }

  /**
   * Internal function for whether to use local or session storage.
   * @param {Object} storage
   *   Use non-persistent storage (sessionStorage)
   *   or persistent storage (localStorage).
   * @returns {Object} A local storage or session storage instance.
   */
  function _getStorageType( storage ) {
    // Use default setting if none is provided.
    if ( typeof storage !== 'object' ) {
      if ( typeof _storage === 'undefined' ) {
        try {
          storage = window.sessionStorage;
        } catch( err ) {
          // SecurityError was thrown if cookies are off.
          storage = {};
        }
      } else {
        storage = _storage;
      }
    }

    return storage;
  }

  // Expose public methods.
  module.exports = {
    setItem:    setItem,
    getItem:    getItem,
    removeItem: removeItem,
    setStorage: setStorage
  };


/***/ },
/* 23 */
/***/ function(module, exports, __webpack_require__) {

  'use strict';

  // Required modules.
  var atomicHelpers = __webpack_require__( 2 );
  var breakpointState = __webpack_require__( 4 );
  var ClearableInput = __webpack_require__( 24 );
  var EventObserver = __webpack_require__( 7 );
  var FlyoutMenu = __webpack_require__( 25 );
  var MoveTransition = __webpack_require__( 29 );

  /**
   * GlobalSearch
   * @class
   *
   * @classdesc Initializes a new GlobalSearch molecule.
   *
   * @param {HTMLNode} element
   *   The DOM element within which to search for the molecule.
   * @returns {GlobalSearch} An instance.
   */
  function GlobalSearch( element ) { // eslint-disable-line max-statements, no-inline-comments, max-len

    var BASE_CLASS = 'm-global-search';

    var _dom = atomicHelpers.checkDom( element, BASE_CLASS, 'GlobalSearch' );
    var _triggerSel = '.' + BASE_CLASS + '_trigger';
    var _triggerDom = _dom.querySelector( _triggerSel );
    var _contentDom = _dom.querySelector( '.' + BASE_CLASS + '_content' );
    var _flyoutMenu = new FlyoutMenu( _dom );
    var _searchInputDom;
    var _searchBtnDom;
    var _clearBtnDom;

    // TODO: Move tab trigger to its own class.
    var _tabTriggerDom =
      _contentDom.querySelector( '.' + BASE_CLASS + '_tab-trigger' );

    var KEY_TAB = 9;

    /**
     * @returns {Object} The GlobalSearch instance.
     */
    function init() {
      // Set initial appearance.
      var transition = new MoveTransition( _contentDom ).init();
      transition.moveRight();
      _flyoutMenu.setExpandTransition( transition, transition.moveToOrigin );
      _flyoutMenu.setCollapseTransition( transition, transition.moveRight );
      _flyoutMenu.init();

      _contentDom.classList.remove( 'u-hidden' );

      var clearBtnSel = '.' + BASE_CLASS + ' .input-contains-label_after__clear';
      var inputContainsLabelSel =
        '.' + BASE_CLASS + '_content-form .input-contains-label';
      var searchBtnSel = '.' + BASE_CLASS + ' .input-with-btn_btn button';

      _clearBtnDom = _contentDom.querySelector( clearBtnSel );
      var inputContainsLabel = _contentDom.querySelector( inputContainsLabelSel );
      _searchInputDom = inputContainsLabel.querySelector( 'input' );
      _searchBtnDom = _contentDom.querySelector( searchBtnSel );

      // Initialize new clearable input behavior on the input-contains-label.
      var clearableInput = new ClearableInput( inputContainsLabel );
      clearableInput.init();

      var handleExpandBeginBinded = _handleExpandBegin.bind( this );
      _flyoutMenu.addEventListener( 'expandBegin', handleExpandBeginBinded );
      _flyoutMenu.addEventListener( 'collapseBegin', _handleCollapseBegin );
      _flyoutMenu.addEventListener( 'collapseEnd', _handleCollapseEnd );

      _tabTriggerDom.addEventListener( 'keyup', _handleTabPress );

      // Set initial collapse state.
      _handleCollapseEnd();

      return this;
    }

    /**
     * Event handler for when there's a click on the page's body.
     * Used to close the global search, if needed.
     * @param {MouseEvent} event The event object for the mousedown event.
     */
    function _handleBodyClick( event ) {
      var target = event.target;

      var isInDesktop = _isInDesktop();
      if ( isInDesktop && !_isDesktopTarget( target ) ||
           !isInDesktop && !_isMobileTarget( target ) ) {
        collapse();
      }
    }

    // TODO: Move this to breakpoint-state.js.
    /**
     * Whether currently in the desktop view.
     * @returns {boolean} True if in the desktop view, otherwise false.
     */
    function _isInDesktop() {
      return true;
    }

    /**
     * Whether a target is one of the ones that appear in the desktop view.
     * @param {HTMLNode} target - The target of a mouse event (most likely).
     * @returns {boolean} True if the passed target is in the desktop view.
     */
    function _isDesktopTarget( target ) {
      return target === _searchInputDom ||
             target === _searchBtnDom ||
             target === _clearBtnDom;
    }

    /**
     * Whether a target is one of the ones that appear in the mobile view.
     * @param {HTMLNode} target - The target of a mouse event (most likely).
     * @returns {boolean} True if the passed target is in the mobile view.
     */
    function _isMobileTarget( target ) {
      return _dom.contains( target );
    }

    /**
     * Event handler for when the tab key is pressed.
     * @param {KeyboardEvent} event
     *   The event object for the keyboard key press.
     */
    function _handleTabPress( event ) {
      if ( event.keyCode === KEY_TAB ) {
        collapse();
      }
    }

    /**
     * Event handler for when FlyoutMenu expand transition begins.
     * Use this to perform post-expandBegin actions.
     */
    function _handleExpandBegin() {
      this.dispatchEvent( 'expandBegin', { target: this } );
      // If it's the desktop view, hide the "Search" button.
      if ( _isInDesktop() ) { _triggerDom.classList.add( 'u-hidden' ); }
      _contentDom.classList.remove( 'u-invisible' );
      _searchInputDom.select();

      document.body.addEventListener( 'mousedown', _handleBodyClick );
    }

    /**
     * Event handler for when FlyoutMenu collapse transition begins.
     * Use this to perform post-collapseBegin actions.
     */
    function _handleCollapseBegin() {
      _triggerDom.classList.remove( 'u-hidden' );
      document.body.removeEventListener( 'mousedown', _handleBodyClick );
    }

    /**
     * Event handler for when FlyoutMenu collapse transition ends.
     * Use this to perform post-collapseEnd actions.
     */
    function _handleCollapseEnd() {
      // TODO: When tabbing is used to collapse the search flyout
      //       it will not animate with the below line.
      //       Investigate why this is the case for tab key
      //       but not with mouse clicks.
      _contentDom.classList.add( 'u-invisible' );
    }

    /**
     * Open the search box.
     * @returns {Object} An GlobalSearch instance.
     */
    function expand() {
      _flyoutMenu.expand();

      return this;
    }

    /**
     * Close the search box.
     * @returns {Object} An GlobalSearch instance.
     */
    function collapse() {
      _flyoutMenu.collapse();

      return this;
    }

    // Attach public events.
    var eventObserver = new EventObserver();
    this.addEventListener = eventObserver.addEventListener;
    this.removeEventListener = eventObserver.removeEventListener;
    this.dispatchEvent = eventObserver.dispatchEvent;

    this.init = init;
    this.expand = expand;
    this.collapse = collapse;

    return this;
  }

  module.exports = GlobalSearch;


/***/ },
/* 24 */
/***/ function(module, exports, __webpack_require__) {

  'use strict';

  // Required modules.
  var atomicHelpers = __webpack_require__( 2 );

  /**
   * ClearableInput
   * @class
   *
   * @classdesc Initializes a new ClearableInput molecule.
   *
   * @param {HTMLNode} element
   *   The DOM element within which to search for the molecule.
   * @returns {Object} A ClearableInput instance.
   */
  function ClearableInput( element ) {
    var BASE_CLASS = 'input-contains-label';

    var _dom = atomicHelpers.checkDom( element, BASE_CLASS, 'ClearableInput' );
    var _inputDom = _dom.querySelector( 'input' );
    var _clearBtnDom = _dom.querySelector( '.' + BASE_CLASS + '_after__clear' );

    var _isClearShowing = true;

    /**
     * @returns {Object} The ClearableInput instance.
     */
    function init() {
      _clearBtnDom.addEventListener( 'mousedown', _clearClicked );
      _inputDom.addEventListener( 'keyup', _inputTyped );

      _setClearBtnState( _inputDom.value );

      return this;
    }

    /**
     * Event handler for when the clear input label was clicked.
     * @param {MouseEvent} event - The event object for the mousedown event.
     */
    function _clearClicked( event ) {
      _inputDom.value = _setClearBtnState( '' );
      _inputDom.focus();

      // Prevent event bubbling up to the input, which would blur otherwise.
      event.preventDefault();
    }

    /**
     * Event handler for when the user typed in the input.
     */
    function _inputTyped() {
      _setClearBtnState( _inputDom.value );
    }

    /**
     * @param {string} value - The input value in the search box.
     * @returns {string} The input value in the search box.
     */
    function _setClearBtnState( value ) {
      if ( _isClearShowing && value === '' ) {
        _hideClearBtn();
      } else if ( !_isClearShowing ) {
        _showClearBtn();
      }
      return value;
    }

    /**
     * Add a hidden class to the input search label.
     * Used when there is no text input.
     */
    function _hideClearBtn() {
      _clearBtnDom.classList.add( 'u-hidden' );
      _isClearShowing = false;
    }

    /**
     * Remove a hidden class from the input search label.
     * Used when there is text input.
     */
    function _showClearBtn() {
      _clearBtnDom.classList.remove( 'u-hidden' );
      _isClearShowing = true;
    }

    this.init = init;

    return this;
  }

  module.exports = ClearableInput;


/***/ },
/* 25 */
/***/ function(module, exports, __webpack_require__) {

  'use strict';

  // Required modules.
  var BaseTransition = __webpack_require__( 26 );
  var dataHook = __webpack_require__( 27 );
  var EventObserver = __webpack_require__( 7 );
  var standardType = __webpack_require__( 28 );

  /**
   * FlyoutMenu
   * @class
   *
   * @classdesc Initializes new FlyoutMenu behavior.
   * As added JS behavior, this is added through HTML data-js-hook attributes.
   *
   * Structure is:
   * flyout-menu
   *   flyout-menu_trigger
   *   flyout-menu_content
   *     flyout-menu_alt-trigger
   *
   * The alt-trigger is for a back button, which may obscure the first trigger.
   * The flyout can be triggered three ways: through a click of the trigger or
   * through the click of an alt-trigger.
   *
   * @param {HTMLNode} element - The DOM element to attach FlyoutMenu behavior.
   * @returns {FlyoutMenu} An instance.
   */
  function FlyoutMenu( element ) { // eslint-disable-line max-statements, no-inline-comments, max-len

    var BASE_CLASS = 'behavior_flyout-menu';
    var SEL_PREFIX = '[' + standardType.JS_HOOK + '=' + BASE_CLASS;

    var BASE_SEL = SEL_PREFIX + ']';
    var ALT_TRIGGER_SEL = SEL_PREFIX + '_alt-trigger]';
    var CONTENT_SEL = SEL_PREFIX + '_content]';
    var TRIGGER_SEL = SEL_PREFIX + '_trigger]';

    // TODO: Update atomic-helpers to support CSS selectors for validity check.
    var _dom = dataHook.contains( element, BASE_CLASS ) ? element : null;
    if ( !_dom ) _dom = element.parentNode.querySelector( BASE_SEL );
    if ( !_dom ) { throw new Error( 'Selector not found on passed node!' ); }

    var _triggerDom = _dom.querySelector( TRIGGER_SEL );
    var _contentDom = _dom.querySelector( CONTENT_SEL );

    if ( !_triggerDom ) { throw new Error( TRIGGER_SEL + ' is missing!' ); }
    if ( !_contentDom ) { throw new Error( CONTENT_SEL + ' is missing!' ); }

    var _altTriggerDom = _dom.querySelector( ALT_TRIGGER_SEL );

    var _isExpanded = false;
    var _isAnimating = false;

    var _expandTransition;
    var _collapseTransition;
    var _expandTransitionMethod;
    var _expandTransitionMethodArgs = [];
    var _collapseTransitionMethod;
    var _collapseTransitionMethodArgs = [];

    // Binded events.
    var _collapseBinded = collapse.bind( this );
    // Needed to add and remove events to transitions.
    var _collapseEndBinded = _collapseEnd.bind( this );
    var _expandEndBinded = _expandEnd.bind( this );

    // If this menu appears in a data source,
    // this can be used to store the source.
    // Examples include the index in an Array,
    // a key in an Hash, or a node in a Tree.
    var _data;

    // Set this function to a queued collapse function,
    // which is called if collapse is called while
    // expand is animating.
    var _deferFunct = standardType.noopFunct;

    // Whether this instance's behaviors are suspended or not.
    var _suspended = true;

    // TODO: Add param to set the FlyoutMenu open at initialization-time.
    /**
     * @returns {FlyoutMenu} An instance.
     */
    function init() {
      // Ignore Google Analytics on the trigger if it is a link,
      // since we're preventing the default link behavior.
      if ( _triggerDom.tagName === 'A' ) {
        _triggerDom.setAttribute( 'data-gtm_ignore', 'true' );
      }

      var triggerClickedBinded = _triggerClicked.bind( this );
      var triggerOverBinded = _triggerOver.bind( this );
      _triggerDom.addEventListener( 'click', triggerClickedBinded );
      _triggerDom.addEventListener( 'mouseover', triggerOverBinded );

      if ( _altTriggerDom ) {
        // If menu contains a submenu but doesn't have
        // its own alternative trigger (such as a Back button),
        // then the altTriggerDom may be in the submenu and we
        // need to remove the reference.
        var subMenu = _dom.querySelector( BASE_SEL );
        if ( subMenu && subMenu.contains( _altTriggerDom ) ) {
          _altTriggerDom = null;
        } else {
          // TODO: Investigate just having multiple triggers,
          //       instead of a primary and alternative.
          // Ignore Google Analytics on the trigger if it is a link,
          // since we're preventing the default link behavior.
          if ( _altTriggerDom.tagName === 'A' ) {
            _altTriggerDom.setAttribute( 'data-gtm_ignore', 'true' );
          }
          // TODO: alt trigger should probably listen for a mouseover event too.
          _altTriggerDom.addEventListener( 'click', triggerClickedBinded );
        }
      }

      resume();

      return this;
    }

    /**
     * Event handler for when the search input trigger is hovered over.
     * @param {HTMLNode} elem - The element to set.
     * @param {boolean} value - The value to set on `aria-expanded`,
     *   casts to a string.
     * @param {string} The cast value.
     */
    function _setAriaExpandedAttr( elem, value ) {
      var strValue = String( value );
      elem.setAttribute( 'aria-expanded', strValue );
      return strValue;
    }

    /**
     * Event handler for when the search input trigger is hovered over.
     */
    function _triggerOver() {
      if ( !_suspended ) {
        this.dispatchEvent( 'triggerOver',
                            { target: this, type: 'triggerOver' } );
      }
    }

    /**
     * Event handler for when the search input trigger is clicked,
     * which opens/closes the search input.
     * @param {MouseEvent} event - The flyout trigger was clicked.
     */
    function _triggerClicked( event ) {
      if ( !_suspended ) {
        this.dispatchEvent( 'triggerClick',
                            { target: this, type: 'triggerClick' } );
        event.preventDefault();
        if ( _isExpanded ) {
          this.collapse();
        } else {
          this.expand();
        }
      }
    }

    /**
     * Open the search box.
     * @returns {FlyoutMenu} An instance.
     */
    function expand() {
      if ( !_isExpanded && !_isAnimating ) {
        _isAnimating = true;
        _deferFunct = standardType.noopFunct;
        this.dispatchEvent( 'expandBegin',
                            { target: this, type: 'expandBegin' } );
        if ( _expandTransitionMethod ) {
          var hasTransition = _expandTransition &&
                              _expandTransition.isAnimated();
          if ( hasTransition ) {
            _expandTransition
              .addEventListener( BaseTransition.END_EVENT, _expandEndBinded );
          }
          _expandTransitionMethod
            .apply( _expandTransition, _expandTransitionMethodArgs );
          if ( !hasTransition ) {
            _expandEndBinded();
          }
        } else {
          _expandEndBinded();
        }
      }

      return this;
    }

    /**
     * Close the search box.
     * If collapse is called when expand animation is underway,
     * save a deferred call to collapse, which is called when
     * expand completes.
     * @returns {FlyoutMenu} An instance.
     */
    function collapse() {
      if ( _isExpanded && !_isAnimating ) {
        _deferFunct = standardType.noopFunct;
        _isAnimating = true;
        _isExpanded = false;
        this.dispatchEvent( 'collapseBegin',
                            { target: this, type: 'collapseBegin' } );
        if ( _collapseTransitionMethod ) {
          var hasTransition = _collapseTransition &&
                              _collapseTransition.isAnimated();
          if ( hasTransition ) {
            _collapseTransition
              .addEventListener( BaseTransition.END_EVENT, _collapseEndBinded );
          }
          _collapseTransitionMethod
            .apply( _collapseTransition, _collapseTransitionMethodArgs );
          if ( !hasTransition ) {
            _collapseEndBinded();
          }
        } else {
          _collapseEndBinded();
        }
        if ( _altTriggerDom ) _setAriaExpandedAttr( _altTriggerDom, false );
        _setAriaExpandedAttr( _triggerDom, false );
        _setAriaExpandedAttr( _contentDom, false );
        // TODO: Remove or uncomment when keyboard navigation is in.
        // _triggerDom.focus();
      } else {
        _deferFunct = _collapseBinded;
      }

      return this;
    }

    /**
     * Expand animation has completed.
     * Call deferred collapse function,
     * if set (otherwise it will call a noop function).
     */
    function _expandEnd() {
      _isAnimating = false;
      _isExpanded = true;
      if ( _expandTransition ) {
        _expandTransition
          .removeEventListener( BaseTransition.END_EVENT, _expandEndBinded );
      }
      this.dispatchEvent( 'expandEnd', { target: this, type: 'expandEnd' } );
      if ( _altTriggerDom ) _setAriaExpandedAttr( _altTriggerDom, true );
      _setAriaExpandedAttr( _triggerDom, true );
      _setAriaExpandedAttr( _contentDom, true );
      // Call collapse, if it was called while expand was animating.
      _deferFunct();
    }

    /**
     * Collapse animation has completed.
     */
    function _collapseEnd() {
      _isAnimating = false;
      if ( _collapseTransition ) {
        _collapseTransition
          .removeEventListener( BaseTransition.END_EVENT, _collapseEndBinded );
      }
      this.dispatchEvent( 'collapseEnd', { target: this, type: 'collapseEnd' } );
    }

    /**
     * @param {MoveTransition|AlphaTransition} transition
     *   A transition instance to watch for events on.
     * @param {Function} method
     *   The transition method to call on expand.
     * @param {Array} args
     *   (Optional) list of arguments to apply to collapse method.
     */
    function setExpandTransition( transition, method, args ) {
      _expandTransition = transition;
      _expandTransitionMethod = method;
      _expandTransitionMethodArgs = args;
    }

    /**
     * @param {MoveTransition|AlphaTransition} transition
     *   A transition instance to watch for events on.
     * @param {Function} method
     *   The transition method to call on collapse.
     * @param {Array} args
     *   (Optional) list of arguments to apply to collapse method.
     */
    function setCollapseTransition( transition, method, args ) {
      _collapseTransition = transition;
      _collapseTransitionMethod = method;
      _collapseTransitionMethodArgs = args;
    }

    /**
     * @param {string} type
     *   (Optional) The type of transition to return.
     *   Accepts 'expand' or 'collapse'.
     *   `FlyoutMenu.EXPAND_TYPE` and `FlyoutMenu.COLLAPSE_TYPE` can be used
     *   as type-safe constants passed into this method.
     *   If neither or something else is supplied, expand type is returned.
     * @returns {MoveTransition|AlphaTransition}
     *   A transition instance set on this instance, or undefined if none is set.
     */
    function getTransition( type ) {
      if ( type === FlyoutMenu.COLLAPSE_TYPE ) {
        return _collapseTransition;
      }

      return _expandTransition;
    }

    /**
     * @returns {Object}
     *   Hash of trigger, alternative trigger, and content DOM references.
     */
    function getDom() {
      return {
        altTrigger: _altTriggerDom,
        container:  _dom,
        content:    _contentDom,
        trigger:    _triggerDom
      };
    }

    /**
     * Enable broadcasting of trigger events.
     * @returns {boolean} True if resumed, false otherwise.
     */
    function resume() {
      if ( _suspended ) {
        _suspended = false;
      }

      return !_suspended;
    }

    /**
     * Suspend broadcasting of trigger events.
     * @returns {boolean} True if suspended, false otherwise.
     */
    function suspend() {
      if ( !_suspended ) {
        _suspended = true;
      }

      return _suspended;
    }

    // TODO: Use Object.defineProperty to create a getter/setter.
    //       See https://github.com/cfpb/cfgov-refresh/pull/1566/
    //           files#diff-7a844d22219d7d3db1fa7c1e70d7ba45R35
    /**
     * @returns {number|string|Object} A data identifier such as an Array index,
     *   Hash key, or Tree node.
     */
    function getData() {
      return _data;
    }

    /**
     * @param {number|string|Object} data
     *   A data identifier such as an Array index, Hash key, or Tree node.
     * @returns {FlyoutMenu} An instance.
     */
    function setData( data ) {
      _data = data;

      return this;
    }

    /**
     * @returns {boolean} True if menu is animating, false otherwise.
     */
    function isAnimating() {
      return _isAnimating;
    }

    /**
     * @returns {boolean} True if menu is expanded, false otherwise.
     */
    function isExpanded() {
      return _isExpanded;
    }

    // Attach public events.
    var eventObserver = new EventObserver();
    this.addEventListener = eventObserver.addEventListener;
    this.removeEventListener = eventObserver.removeEventListener;
    this.dispatchEvent = eventObserver.dispatchEvent;

    this.init = init;
    this.expand = expand;
    this.collapse = collapse;
    this.setExpandTransition = setExpandTransition;
    this.setCollapseTransition = setCollapseTransition;
    this.getData = getData;
    this.getTransition = getTransition;
    this.getDom = getDom;
    this.isAnimating = isAnimating;
    this.isExpanded = isExpanded;
    this.resume = resume;
    this.setData = setData;
    this.suspend = suspend;

    // Public static properties.
    FlyoutMenu.EXPAND_TYPE = 'expand';
    FlyoutMenu.COLLAPSE_TYPE = 'collapse';
    FlyoutMenu.BASE_CLASS = BASE_CLASS;
    FlyoutMenu.BASE_SEL = BASE_SEL;
    FlyoutMenu.ALT_TRIGGER_SEL = ALT_TRIGGER_SEL;
    FlyoutMenu.CONTENT_SEL = CONTENT_SEL;
    FlyoutMenu.TRIGGER_SEL = TRIGGER_SEL;

    return this;
  }

  module.exports = FlyoutMenu;


/***/ },
/* 26 */
/***/ function(module, exports, __webpack_require__) {

  'use strict';

  // Required modules.
  var EventObserver = __webpack_require__( 7 );

  /**
   * BaseTransition
   * @class
   *
   * @classdesc Initializes new BaseTransition behavior.
   *   This shouldn't be used directly, but instead should be
   *   the base class used through composition by a specific transition.
   *
   * @param {HTMLNode} element
   *   DOM element to apply transition to.
   * @param {Object} classes
   *   The classes to apply to this transition.
   * @returns {BaseTransition} An instance.
   */
  function BaseTransition( element, classes ) { // eslint-disable-line max-statements, no-inline-comments, max-len
    var _classes = classes;
    var _dom;

    var _lastClass;
    var _transitionEndEvent;
    var _transitionCompleteBinded = _transitionComplete.bind( this );
    var _addEventListenerBinded = _addEventListener.bind( this );
    var _isFlushed = false;

    /**
     * @returns {BaseTransition} An instance.
     */
    function init() {
      setElement( element );

      return this;
    }

    /**
     * Add an event listener to the transition, or call the transition
     * complete handler immediately if transition not supported.
     * @param {HTMLNode} elem - Set the HTML element target of this transition.
     */
    function setElement( elem ) {
      // If the element has already been set,
      // clear the transition classes from the old element.
      if ( _dom ) {
        remove();
        animateOn();
      }
      _dom = elem;
      _dom.classList.add( _classes.BASE_CLASS );
      _transitionEndEvent = _getTransitionEndEvent( _dom );
    }

    /**
     * Add a "transition-duration: 0s" utility CSS class.
     */
    function animateOn() {
      _dom.classList.remove( BaseTransition.NO_ANIMATION_CLASS );
    }

    /**
     * Remove a "transition-duration: 0s" utility CSS class.
     */
    function animateOff() {
      _dom.classList.add( BaseTransition.NO_ANIMATION_CLASS );
    }

    /**
     * @returns {boolean} Whether the transition has a duration or not.
     */
    function isAnimated() {
      return !_dom.classList.contains( BaseTransition.NO_ANIMATION_CLASS );
    }

    /**
     * Add an event listener to the transition, or call the transition
     * complete handler immediately if transition not supported.
     */
    function _addEventListener() {
      // If transition is not supported, call handler directly (IE9/OperaMini).
      if ( _transitionEndEvent ) {
        _dom.addEventListener( _transitionEndEvent,
                                          _transitionCompleteBinded );
        this.dispatchEvent( BaseTransition.BEGIN_EVENT, { target: this } );
      } else {
        this.dispatchEvent( BaseTransition.BEGIN_EVENT, { target: this } );
        _transitionCompleteBinded();
      }
    }

    /**
     * Remove an event listener to the transition.
     */
    function _removeEventListener() {
      _dom.removeEventListener( _transitionEndEvent, _transitionCompleteBinded );
    }

    /**
     * Handle the end of a transition.
     */
    function _transitionComplete() {
      _removeEventListener();
      this.dispatchEvent( BaseTransition.END_EVENT, { target: this } );
    }

    /**
     * Search for and remove initial BaseTransition classes that have
     * already been applied to this BaseTransition's target element.
     */
    function _flush() {
      for ( var prop in _classes ) {
        if ( _classes.hasOwnProperty( prop ) &&
             _classes[prop] !== _classes.BASE_CLASS &&
             _dom.classList.contains( _classes[prop] ) ) {
          _dom.classList.remove( _classes[prop] );
        }
      }
    }

    /**
     * Remove all transition classes.
     */
    function remove() {
      _dom.classList.remove( _classes.BASE_CLASS );
      _flush();
    }

    /**
     * @param {string} className - A CSS class.
     * @returns {boolean} False if the class is already applied,
     *   otherwise true if the class was applied.
     */
    function applyClass( className ) {
      if ( !_isFlushed ) {
        _flush();
        _isFlushed = true;
      }

      if ( _dom.classList.contains( className ) ) {
        return false;
      }

      _removeEventListener();
      _dom.classList.remove( _lastClass );
      _lastClass = className;
      _addEventListenerBinded();
      _dom.classList.add( _lastClass );

      return true;
    }

    // TODO: Update Expandables to use a transition.
    /**
     * @param {HTMLNode} elem
     *   The element to check for support of transition end event.
     * @returns {string} The browser-prefixed transition end event.
     */
    function _getTransitionEndEvent( elem ) {
      if ( !elem ) {
        var msg = 'Element does not have TransitionEnd event. It may be null!';
        throw new Error( msg );
      }

      var transition;
      var transitions = {
        WebkitTransition: 'webkitTransitionEnd',
        MozTransition:    'transitionend',
        OTransition:      'oTransitionEnd otransitionend',
        transition:       'transitionend'
      };

      for ( var t in transitions ) {
        if ( transitions.hasOwnProperty( t ) &&
             typeof elem.style[t] !== 'undefined' ) {
          transition = transitions[t];
          break;
        }
      }
      return transition;
    }

    // Attach public events.
    var eventObserver = new EventObserver();
    this.addEventListener = eventObserver.addEventListener;
    this.dispatchEvent = eventObserver.dispatchEvent;
    this.removeEventListener = eventObserver.removeEventListener;

    this.animateOff = animateOff;
    this.animateOn = animateOn;
    this.applyClass = applyClass;
    this.init = init;
    this.isAnimated = isAnimated;
    this.remove = remove;
    this.setElement = setElement;

    return this;
  }

  // Public static constants.
  BaseTransition.BEGIN_EVENT = 'transitionBegin';
  BaseTransition.END_EVENT = 'transitionEnd';
  BaseTransition.NO_ANIMATION_CLASS = 'u-no-animation';

  module.exports = BaseTransition;


/***/ },
/* 27 */
/***/ function(module, exports, __webpack_require__) {

  'use strict';

  // Required modules.
  var standardType = __webpack_require__( 28 );

  /**
   * @param {HTMLNode} element - DOM element.
   * @param {string} value
   *   Value to add to the element's JS data-* hook.
   * @throws {Error} If supplied value contains a space,
   *   which would mean it would be two values, which is likely a typo.
   * @returns {string} The value that was added.
   */
  function add( element, value ) {
    if ( value.indexOf( ' ' ) !== -1 ) {
      var msg = standardType.JS_HOOK + 'values cannot contain spaces!';
      throw new Error( msg );
    }

    var values = element.getAttribute( standardType.JS_HOOK );
    if ( values !== null ) {
      value = values + ' ' + value;
    }
    element.setAttribute( standardType.JS_HOOK, value );

    return value;
  }

  /**
   * @param {HTMLNode} element - DOM element.
   * @param {string} value
   *   Value to remove from the JS data-* hook value.
   * @returns {boolean} True if value was removed, false otherwise.
   */
  function remove( element, value ) {
    var values = element.getAttribute( standardType.JS_HOOK );
    var index = values.indexOf( value );
    var valuesList = values.split( ' ' );
    if ( index > -1 ) {
      valuesList.splice( index, 1 );
      element.setAttribute( standardType.JS_HOOK, valuesList.join( ' ' ) );
      return true;
    }

    return false;
  }

  /**
   * @param {HTMLNode} element - DOM element.
   * @param {string} value
   *   Value to check as existing as a JS data-* hook value.
   * @returns {boolean} True if the data-* hook value exists, false otherwise.
   */
  function contains( element, value ) {
    var values = element.getAttribute( standardType.JS_HOOK );
    // If JS data-* hook is not set return immediately.
    if ( !values ) { return false; }
    values = values.split( ' ' );

    return values.indexOf( value ) > -1 ? true : false;
  }

  module.exports = {
    add:      add,
    contains: contains,
    remove:   remove
  };


/***/ },
/* 28 */
/***/ function(module, exports) {

  'use strict';

  // Constant for the name of the JS hook used
  // for attaching JS behavior to HTML DOM elements.
  var JS_HOOK = 'data-js-hook';

  /**
   * Empty function that will do nothing.
   * A usecase is when an object has empty functions used for callbacks,
   * which are meant to be overridden with functionality, but if not,
   * noopFunct will fire and do nothing instead.
   *
   * e.g.
   * callback.onComplete = standardType.noopFunct;
   */
  function noopFunct() {
    // Placeholder function meant to be overridden.
  }

  module.exports = {
    JS_HOOK:   JS_HOOK,
    noopFunct: noopFunct
  };


/***/ },
/* 29 */
/***/ function(module, exports, __webpack_require__) {

  'use strict';

  // Required modules.
  var EventObserver = __webpack_require__( 7 );
  var BaseTransition = __webpack_require__( 26 );

  // Exported constants.
  var CLASSES = Object.seal( {
    BASE_CLASS:     'u-move-transition',
    MOVE_TO_ORIGIN: 'u-move-to-origin',
    MOVE_LEFT:      'u-move-left',
    MOVE_LEFT_2X:   'u-move-left-2x',
    MOVE_LEFT_3X:   'u-move-left-3x',
    MOVE_RIGHT:     'u-move-right',
    MOVE_UP:        'u-move-up'
  } );

  /**
   * MoveTransition
   * @class
   *
   * @classdesc Initializes new MoveTransition behavior.
   *
   * @param {HTMLNode} element
   *   DOM element to apply move transition to.
   * @returns {MoveTransition} An instance.
   */
  function MoveTransition( element ) { // eslint-disable-line max-statements, no-inline-comments, max-len

    var _baseTransition = new BaseTransition( element, CLASSES ).init();
    var _transitionCompleteBinded = _transitionComplete.bind( this );
    _baseTransition.addEventListener( BaseTransition.END_EVENT,
                                      _transitionCompleteBinded );

    /**
     * @returns {MoveTransition} An instance.
     */
    function init() {
      return this;
    }

    /**
     * @param {HTMLNode} elem - Set HTML element target of the transition.
     */
    function setElement( elem ) {
      _baseTransition.setElement( elem );
    }

    /**
     * Remove all transition classes.
     */
    function remove() {
      _baseTransition.remove();
    }

    /**
     * Add a "transition-duration: 0" utility CSS class.
     */
    function animateOn() {
      _baseTransition.animateOn();
    }

    /**
     * Remove a "transition-duration: 0" utility CSS class.
     */
    function animateOff() {
      _baseTransition.animateOff();
    }

    /**
     * @returns {boolean} Whether the transition has a duration or not.
     */
    function isAnimated() {
      return _baseTransition.isAnimated();
    }

    /**
     * Handle the end of a transition.
     */
    function _transitionComplete() {
      this.dispatchEvent( BaseTransition.END_EVENT, { target: this } );
    }

    /**
     * Move to the element's original coordinates.
     * @returns {MoveTransition} An instance.
     */
    function moveToOrigin() {
      _baseTransition.applyClass( CLASSES.MOVE_TO_ORIGIN );

      return this;
    }

    /**
     * Move to the left by applying a utility move class.
     * @param {Number} count
     *   How many times to move left as a multiplication of the element's width.
     * @returns {MoveTransition} An instance.
     */
    function moveLeft( count ) {
      count = count || 1;
      var moveClasses = [
        CLASSES.MOVE_LEFT,
        CLASSES.MOVE_LEFT_2X,
        CLASSES.MOVE_LEFT_3X
      ];

      if ( count < 1 || count > moveClasses.length ) {
        throw new Error( 'MoveTransition: moveLeft count is out of range!' );
      }

      _baseTransition.applyClass( moveClasses[count - 1] );

      return this;
    }

    /**
     * Move to the right by applying a utility move class.
     * @returns {MoveTransition} An instance.
     */
    function moveRight() {
      _baseTransition.applyClass( CLASSES.MOVE_RIGHT );

      return this;
    }

    /**
     * Move up by applying a utility move class.
     * @returns {MoveTransition} An instance.
     */
    function moveUp() {
      _baseTransition.applyClass( CLASSES.MOVE_UP );

      return this;
    }

    // Attach public events.
    var eventObserver = new EventObserver();
    this.addEventListener = eventObserver.addEventListener;
    this.dispatchEvent = eventObserver.dispatchEvent;
    this.removeEventListener = eventObserver.removeEventListener;

    this.animateOff = animateOff;
    this.animateOn = animateOn;
    this.init = init;
    this.isAnimated = isAnimated;
    this.moveToOrigin = moveToOrigin;
    this.moveLeft = moveLeft;
    this.moveRight = moveRight;
    this.moveUp = moveUp;
    this.setElement = setElement;
    this.remove = remove;

    return this;
  }

  // Public static properties.
  MoveTransition.CLASSES = CLASSES;

  module.exports = MoveTransition;


/***/ },
/* 30 */
/***/ function(module, exports, __webpack_require__) {

  'use strict';

  // Required modules.
  var atomicHelpers = __webpack_require__( 2 );
  var breakpointState = __webpack_require__( 4 );
  var dataHook = __webpack_require__( 27 );
  var EventObserver = __webpack_require__( 7 );
  var FlyoutMenu = __webpack_require__( 25 );
  var MegaMenuDesktop = __webpack_require__( 31 );
  var MegaMenuMobile = __webpack_require__( 32 );
  var MoveTransition = __webpack_require__( 29 );
  var Tree = __webpack_require__( 34 );

  /**
   * MegaMenu
   * @class
   *
   * @classdesc Initializes a new MegaMenu organism.
   *
   * @param {HTMLNode} element
   *   The DOM element within which to search for the organism.
   * @returns {MegaMenu} An instance.
   */
  function MegaMenu( element ) {
    var BASE_CLASS = 'o-mega-menu';

    var _dom = atomicHelpers.checkDom( element, BASE_CLASS, 'MegaMenu' );

    // Tree data model.
    var _menus;

    // Screen-size specific behaviors.
    var _desktopNav;
    var _mobileNav;

    // TODO: Move tab trigger to its own class.
    var _tabTriggerDom = _dom.querySelector( '.' + BASE_CLASS + '_tab-trigger' );

    var KEY_TAB = 9;

    /**
     * @returns {MegaMenu} An instance.
     */
    function init() {
      // DOM selectors.
      var rootMenuDom = _dom;
      var rootContentDom = rootMenuDom.querySelector( FlyoutMenu.CONTENT_SEL );

      // Create model.
      _menus = new Tree();

      // Create root menu.
      var transition = new MoveTransition( rootContentDom ).init();
      var rootMenu = new FlyoutMenu( rootMenuDom ).init();
      // Set initial position.
      rootMenu.setExpandTransition( transition, transition.moveToOrigin );
      rootMenu.setCollapseTransition( transition, transition.moveLeft );
      _addEvents( rootMenu );

      // Populate tree model with menus.
      var rootNode = _menus.init( rootMenu ).getRoot();
      rootMenu.setData( rootNode );
      _populateTreeFromDom( rootMenuDom, rootNode, _addMenu );

      // Initialize screen-size specific behaviors.
      _desktopNav = new MegaMenuDesktop( _menus ).init();
      _mobileNav = new MegaMenuMobile( _menus ).init();
      _mobileNav.addEventListener( 'rootExpandBegin',
                                   _handleRootExpandBegin.bind( this ) );
      _mobileNav.addEventListener( 'rootCollapseEnd',
                                   _handleRootCollapseEnd.bind( this ) );

      window.addEventListener( 'resize', _resizeHandler );

      if ( _isInDesktop() ) {
        _desktopNav.resume();
      } else {
        _mobileNav.resume();
      }

      _dom.classList.remove( 'u-hidden' );

      _tabTriggerDom.addEventListener( 'keyup', _handleTabPress );

      return this;
    }

    /**
     * Perform a recursive depth-first search of the DOM
     * and call a function for each node.
     * @param {HTMLNode} dom - A DOM element to search from.
     * @param {TreeNode} parentNode
     *   Node in a tree from which to attach new nodes.
     * @param {Function} callback - Function to call on each node.
     *   Must return a TreeNode.
     */
    function _populateTreeFromDom( dom, parentNode, callback ) {
      var children = dom.children;
      var child;
      for ( var i = 0, len = children.length; i < len; i++ ) {
        var newParentNode = parentNode;
        child = children[i];
        newParentNode = callback.call( this, child, newParentNode );
        _populateTreeFromDom( child, newParentNode, callback );
      }
    }

    /**
     * Create a new FlyoutMenu and attach it to a new tree node.
     * @param {HTMLNode} dom
     *   A DOM element to check for a js data-* attribute hook.
     * @param {TreeNode} parentNode
     *   The parent node in a tree on which to attach a new menu.
     * @returns {TreeNode} Return the processed tree node.
     */
    function _addMenu( dom, parentNode ) {
      var newParentNode = parentNode;
      var transition;
      if ( dataHook.contains( dom, FlyoutMenu.BASE_CLASS ) ) {
        var menu = new FlyoutMenu( dom ).init();
        transition = new MoveTransition( menu.getDom().content ).init();
        menu.setExpandTransition( transition, transition.moveToOrigin );
        menu.setCollapseTransition( transition, transition.moveLeft );
        _addEvents( menu );
        newParentNode = newParentNode.tree.add( menu, newParentNode );
        menu.setData( newParentNode );
      }

      return newParentNode;
    }

    /**
     * @param {FlyoutMenu} menu - a menu on which to attach events.
     */
    function _addEvents( menu ) {
      menu.addEventListener( 'triggerOver', _handleEvent );
      menu.addEventListener( 'triggerClick', _handleEvent );
      menu.addEventListener( 'expandBegin', _handleEvent );
      menu.addEventListener( 'expandEnd', _handleEvent );
      menu.addEventListener( 'collapseBegin', _handleEvent );
      menu.addEventListener( 'collapseEnd', _handleEvent );
    }

    /**
     * Handle events coming from menu,
     * and pass it to the desktop or mobile behaviors.
     * @param {Object} event - A FlyoutMenu event object.
     */
    function _handleEvent( event ) {
      var activeNav = _isInDesktop() ? _desktopNav : _mobileNav;
      activeNav.handleEvent( event );
    }

    /**
     * Handle resizing of the window,
     * suspends or resumes the mobile or desktop menu behaviors.
     */
    function _resizeHandler() {
      if ( _isInDesktop() ) {
        _mobileNav.suspend();
        _desktopNav.resume();
      } else {
        _desktopNav.suspend();
        _mobileNav.resume();
      }
    }

    // TODO: Move this to breakpoint-state.js.
    /**
     * Whether currently in the desktop view.
     * @returns {boolean} True if in the desktop view, otherwise false.
     */
    function _isInDesktop() {
      return true;
    }

    /**
     * Event handler for when the tab key is pressed.
     * @param {KeyboardEvent} event
     *   The event object for the keyboard key press.
     */
    function _handleTabPress( event ) {
      if ( event.keyCode === KEY_TAB ) {
        collapse();
      }
    }

    /**
     * Close the mega menu.
     * @returns {MegaMenu} An instance.
     */
    function collapse() {
      if ( !_isInDesktop() ) {
        _mobileNav.collapse();
      }

      return this;
    }

    /**
     * Event handler for when root menu expand transition begins.
     */
    function _handleRootExpandBegin() {
      this.dispatchEvent( 'rootExpandBegin', { target: this } );
    }

    /**
     * Event handler for when root menu collapse transition ends.
     */
    function _handleRootCollapseEnd() {
      this.dispatchEvent( 'rootCollapseEnd', { target: this } );
    }

    // Attach public events.
    var eventObserver = new EventObserver();
    this.addEventListener = eventObserver.addEventListener;
    this.removeEventListener = eventObserver.removeEventListener;
    this.dispatchEvent = eventObserver.dispatchEvent;

    this.init = init;
    this.collapse = collapse;

    return this;
  }

  module.exports = MegaMenu;


/***/ },
/* 31 */
/***/ function(module, exports, __webpack_require__) {

  'use strict';

  // Required modules.
  var EventObserver = __webpack_require__( 7 );
  var MoveTransition = __webpack_require__( 29 );

  /**
   * MegaMenuDesktop
   * @class
   *
   * @classdesc Behavior for the mega menu at desktop sizes.
   *
   * @param {Tree} menus - Tree of FlyoutMenus.
   * @returns {MegaMenuDesktop} An instance.
   */
  function MegaMenuDesktop( menus ) {

    // DOM references.
    var _bodyDom = document.body;

    // Binded functions.
    var _handleTriggerClickBinded = _handleTriggerClick.bind( this );
    var _handleTriggerOverBinded = _handleTriggerOver.bind( this );
    var _handleExpandBeginBinded = _handleExpandBegin.bind( this );
    var _handleCollapseEndBinded = _handleCollapseEnd.bind( this );

    // Tree model.
    var _menus = menus;

    //  Currently showing menu picked from the tree.
    var _activeMenu = null;

    // Whether this instance's behaviors are suspended or not.
    var _suspended = true;

    /**
     * @returns {MegaMenuDesktop} An instance.
     */
    function init() {

      return this;
    }

    /**
     * Pass an event bubbled up from the menus to the appropriate handler.
     * @param {Event} event - A FlyoutMenu event.
     */
    function handleEvent( event ) {
      if ( !_suspended ) {
        if ( event.type === 'triggerClick' ) {
          _handleTriggerClickBinded( event );
        } else if ( event.type === 'triggerOver' ) {
          _handleTriggerOverBinded( event );
        } else if ( event.type === 'expandBegin' ) {
          _handleExpandBeginBinded( event );
        } else if ( event.type === 'collapseEnd' ) {
          _handleCollapseEndBinded( event );
        }
      }
    }

    /**
     * Event handler for when FlyoutMenu trigger is clicked.
     * @param {Event} event - A FlyoutMenu event.
     */
    function _handleTriggerClick( event ) {
      this.dispatchEvent( 'triggerClick', { target: this } );
      var menu = event.target;
      if ( !menu.isAnimating() ) {
        if ( _activeMenu === null ) {
          // A menu is opened.
          _activeMenu = menu;
          _activeMenu.getTransition().animateOn();
          // TODO: Investigate whether mouseout event may be able to be used
          //       instead of mousemove.
          _bodyDom.addEventListener( 'mousemove', _handleMove );
          _bodyDom.addEventListener( 'mouseleave', _handleMove );
        } else if ( _activeMenu === menu ) {
          // A menu is closed.
          _activeMenu.getTransition().animateOn();
          _activeMenu = null;
          _bodyDom.removeEventListener( 'mousemove', _handleMove );
          _bodyDom.removeEventListener( 'mouseleave', _handleMove );
        } else {
          // An open menu has switched to another menu.
          _activeMenu.getTransition().animateOff();
          _activeMenu.collapse();
          _activeMenu = event.target;
          _activeMenu.getTransition().animateOff();
        }
      }
    }

    /**
     * Event handler for when FlyoutMenu expand transition begins.
     * Use this to perform post-expandBegin actions.
     */
    function _handleExpandBegin() {
      this.dispatchEvent( 'expandBegin', { target: this } );

      // Set keyboard focus on first menu item link.
      var activeMenuDom = _activeMenu.getDom().content;
      activeMenuDom.classList.remove( 'u-invisible' );
      // TODO: Remove or uncomment when keyboard navigation is in.
      // var firstMenuLink = activeMenuDom.querySelector( 'a' );
      // firstMenuLink.focus();
    }

    /**
     * Event handler for when FlyoutMenu collapse transition has ended.
     * Use this to perform post-collapseEnd actions.
     * @param {Event} event - A FlyoutMenu event.
     */
    function _handleCollapseEnd( event ) {
      this.dispatchEvent( 'collapseEnd', { target: this } );
      event.target.getDom().content.classList.add( 'u-invisible' );
    }

    /**
     * Event handler for when FlyoutMenu trigger is hovered over.
     * @param {Event} event - A FlyoutMenu event.
     */
    function _handleTriggerOver( event ) {
      this.dispatchEvent( 'triggerOver', { target: this } );
      var menu = event.target;
      var level = menu.getData().level;

      // Only trigger a click when rolling over the level one
      // menu items when in the desktop view.
      if ( level === 1 && _activeMenu !== menu ) {
        menu.getDom().trigger.click();
      }
    }

    /**
     * Event handler for when mouse is hovering.
     * @param {MouseEvent} event - The hovering event.
     */
    function _handleMove( event ) {
      var menu = event.target;

      if ( !_activeMenu.getDom().container.parentNode.contains( menu ) ) {
        _activeMenu.getDom().trigger.click();
      }
    }

    /**
     * Add events necessary for the desktop menu behaviors.
     * @returns {boolean} Whether it has successfully been resumed or not.
     */
    function resume() {
      if ( _suspended ) {
        var level2 = _menus.getAllAtLevel( 1 );
        var menu;
        var contentDom;
        var wrapperDom;
        var wrapperSel = '.o-mega-menu_content-2-wrapper';
        var transition;
        for ( var i = 0, len = level2.length; i < len; i++ ) {
          menu = level2[i].data;
          contentDom = menu.getDom().content;
          wrapperDom = contentDom.querySelector( wrapperSel );
          transition = menu.getTransition();
          // This checks if the transition has been removed by MegaMenuMobile.
          if ( transition ) {
            transition.setElement( wrapperDom );
          } else {
            transition = new MoveTransition( wrapperDom );
          }
          transition.moveUp();
          // TODO: The only reason hiding is necessary is that the
          //       drop-shadow of the menu extends below it border,
          //       so it's still visible when the menu slides -100% out of view.
          //       Investigate whether it would be better to have a u-move-up-1_1x
          //       or similar class to move up -110%. Or whether the drop-shadow
          //       could be included within the bounds of the menu.
          menu.getDom().content.classList.add( 'u-invisible' );
          menu.setExpandTransition( transition, transition.moveToOrigin );
          menu.setCollapseTransition( transition, transition.moveUp );

          // TODO: Investigate whether deferred collapse has another solution.
          //       This check is necessary since a call to an already collapsed
          //       menu will set a deferred collapse that will be called
          //       on expandEnd next time the flyout is expanded.
          //       The deferred collapse is used in cases where the
          //       user clicks the flyout menu while it is animating open,
          //       so that it appears like they can collapse it, even when
          //       clicking during the expand animation.
          if ( menu.isExpanded() ) {
            menu.collapse();
          }
        }

        // TODO: Combine this loop with the above
        //       into a Breadth-First Search iteration.
        var level3 = _menus.getAllAtLevel( 2 );
        for ( var i2 = 0, len2 = level3.length; i2 < len2; i2++ ) {
          level3[i2].data.suspend();
        }

        _suspended = false;
      }

      return !_suspended;
    }

    /**
     * Remove events necessary for the desktop menu behaviors.
     * @returns {boolean} Whether it has successfully been suspended or not.
     */
    function suspend() {
      if ( !_suspended ) {
        var level2 = _menus.getAllAtLevel( 1 );
        var menu;
        var transition;
        for ( var i = 0, len = level2.length; i < len; i++ ) {
          menu = level2[i].data;
          transition = menu.getTransition();
          transition.remove();
          menu.getDom().content.classList.remove( 'u-invisible' );

          if ( menu.isExpanded() ) {
            menu.collapse();
          }
        }

        // TODO: Combine this loop with the above
        //       into a Breadth-First Search iteration.
        var level3 = _menus.getAllAtLevel( 2 );
        for ( var i2 = 0, len2 = level3.length; i2 < len2; i2++ ) {
          level3[i2].data.resume();
        }

        _suspended = true;
      }

      return _suspended;
    }

    // Attach public events.
    var eventObserver = new EventObserver();
    this.addEventListener = eventObserver.addEventListener;
    this.removeEventListener = eventObserver.removeEventListener;
    this.dispatchEvent = eventObserver.dispatchEvent;

    this.handleEvent = handleEvent;
    this.init = init;
    this.resume = resume;
    this.suspend = suspend;

    return this;
  }

  module.exports = MegaMenuDesktop;


/***/ },
/* 32 */
/***/ function(module, exports, __webpack_require__) {

  'use strict';

  // Required modules.
  var EventObserver = __webpack_require__( 7 );
  var MoveTransition = __webpack_require__( 29 );
  var treeTraversal = __webpack_require__( 33 );

  /**
   * MegaMenuMobile
   * @class
   *
   * @classdesc Behavior for the mega menu at desktop sizes.
   *
   * @param {Tree} menus - Tree of FlyoutMenus.
   * @returns {MegaMenuMobile} An instance.
   */
  function MegaMenuMobile( menus ) {

    // DOM references.
    var _bodyDom = document.body;

    // Binded functions.
    var _handleTriggerClickBinded = _handleTriggerClick.bind( this );
    var _handleExpandBeginBinded = _handleExpandBegin.bind( this );
    var _handleCollapseBeginBinded = _handleCollapseBegin.bind( this );
    var _handleCollapseEndBinded = _handleCollapseEnd.bind( this );
    var _suspendBinded = suspend.bind( this );

    // Tree model.
    var _menus = menus;

    var _rootMenu;
    var _rootMenuContentDom;

    //  Currently showing menu picked from the tree.
    var _activeMenu = null;
    var _activeMenuDom;

    // Whether this instance's behaviors are suspended or not.
    var _suspended = true;

    /**
     * @returns {MegaMenuMobile} An instance.
     */
    function init() {

      var rootNode = _menus.getRoot();
      _rootMenu = rootNode.data;
      _rootMenuContentDom = _rootMenu.getDom().content;
      _activeMenu = _rootMenu;
      _activeMenuDom = _rootMenuContentDom;

      return this;
    }

    /**
     * Event handler for when there's a click on the page's body.
     * Used to close the global search, if needed.
     * @param {MouseEvent} event The event object for the mousedown event.
     */
    function _handleBodyClick( event ) {
      var target = event.target;
      if ( _activeMenu.getDom().trigger === target ) {
        return;
      }

      if ( !_rootMenu.getDom().container.contains( target ) ) {
        _rootMenu.getDom().trigger.click();
      }
    }

    /**
     * Pass an event bubbled up from the menus to the appropriate handler.
     * @param {Event} event - A FlyoutMenu event.
     */
    function handleEvent( event ) {
      if ( !_suspended ) {
        if ( event.type === 'triggerClick' ) {
          _handleTriggerClickBinded( event );
        } else if ( event.type === 'expandBegin' ) {
          _handleExpandBeginBinded( event );
        } else if ( event.type === 'collapseBegin' ) {
          _handleCollapseBeginBinded( event );
        } else if ( event.type === 'collapseEnd' ) {
          _handleCollapseEndBinded( event );
        }
      }
    }

    /**
     * Event handler for when FlyoutMenu trigger is clicked.
     * @param {Event} event - A FlyoutMenu event.
     */
    function _handleTriggerClick( event ) {
      this.dispatchEvent( 'triggerClick', { target: this } );
      var menu = event.target;
      var rootMenu = _menus.getRoot().data;
      var menuNode = menu.getData();
      var level = menuNode.level;
      var transition = rootMenu.getTransition();

      if ( menu === rootMenu ) {
        // Root menu clicked.

        // Root menu is closing.
        if ( menu.isExpanded() ) {
          level = _activeMenu.getData().level;
          menu.setCollapseTransition( transition,
                                      transition.moveLeft, [ level + 1 ] );
        }
      } else {
        // Submenu clicked.
        var siblings = _menus.getAllAtLevel( level );
        var siblingMenu;
        for ( var i = 0, len = siblings.length; i < len; i++ ) {
          siblingMenu = siblings[i].data;
          siblingMenu
            .setExpandTransition( transition, transition.moveLeft, [ level ] );
          // If on the 2nd level menu, set the back button to moveToOrigin,
          // otherwise we're on the 3rd level menu, so moveLeft is needed.
          if ( level === 1 ) {
            siblingMenu
              .setCollapseTransition( transition, transition.moveToOrigin );
          } else {
            siblingMenu.setCollapseTransition( transition, transition.moveLeft );
          }
          // If we're on the current menu, show it & hide all the other siblings.
          if ( siblings[i] === menuNode ) {
            siblingMenu.getDom().content.classList.remove( 'u-invisible' );
          } else {
            siblingMenu.getDom().content.classList.add( 'u-invisible' );
          }
        }

        // TODO: Investigate helper functions to mask these crazy long lookups!
        menuNode.parent.data.getDom()
          .content.classList.remove( 'u-hidden-overflow' );
      }
      _activeMenu = menu;
    }

    /**
     * Event handler for when the search input flyout is toggled,
     * which opens/closes the search input.
     * @param {FlyoutMenu} target - menu that is expanding or collapsing.
     */
    function _handleToggle( target ) {
      if ( target === _rootMenu &&
           _activeMenu !== target ) {
        _activeMenu.collapse();
      }
      _activeMenu = target;
      _activeMenuDom = _activeMenu.getDom().content;
    }

    /**
     * Event handler for when FlyoutMenu expand transition begins.
     * Use this to perform post-expandBegin actions.
     * @param {Event} event - A FlyoutMenu event.
     */
    function _handleExpandBegin( event ) {
      var menu = event.target;
      _handleToggle( menu );
      if ( menu === _rootMenu ) {
        this.dispatchEvent( 'rootExpandBegin', { target: this } );
        _bodyDom.addEventListener( 'mousedown', _handleBodyClick );
      }

      // TODO: Enable or remove when keyboard navigation is in.
      // If on a submenu, focus the back button, otherwise focus the first link.
      // var firstMenuLink;
      // if ( _activeMenu === _rootMenu ) {
      //   firstMenuLink = _activeMenuDom.querySelector( 'a' );
      // } else {
      //   firstMenuLink = _activeMenuDom.querySelector( 'button' );
      // }
      // firstMenuLink.focus();
    }

    /**
     * Event handler for when FlyoutMenu collapse transition has begun.
     * Use this to perform post-collapseBegin actions.
     * @param {Event} event - A FlyoutMenu event.
     */
    function _handleCollapseBegin( event ) {
      var menu = event.target;
      _handleToggle( menu );
      if ( menu === _rootMenu ) {
        _bodyDom.removeEventListener( 'mousedown', _handleBodyClick );
      }
    }

    /**
     * Event handler for when FlyoutMenu collapse transition has ended.
     * Use this to perform post-collapseEnd actions.
     * @param {Event} event - A FlyoutMenu event.
     */
    function _handleCollapseEnd( event ) {
      var menu = event.target;
      if ( menu === _rootMenu ) {
        _suspendBinded();
        resume();
      } else {
        // When clicking the back button and sliding to the right,
        // hide the overflow after animation has completed.
        var parentNode = menu.getData().parent;
        parentNode.data.getDom().content.classList.add( 'u-hidden-overflow' );
      }
    }

    /**
     * Close the mega menu.
     * @returns {MegaMenuMobile} A instance.
     */
    function collapse() {
      if ( _rootMenu.isExpanded() ) {
        _rootMenu.getDom().trigger.click();
      }

      return this;
    }

    /**
     * Add events necessary for the desktop menu behaviors.
     * @returns {boolean} Whether it has successfully been resumed or not.
     */
    function resume() {
      if ( _suspended ) {
        var transition = new MoveTransition( _rootMenuContentDom ).init();
        _rootMenu.setExpandTransition( transition, transition.moveToOrigin );
        _rootMenu.setCollapseTransition( transition, transition.moveLeft );
        _rootMenu.getTransition().moveLeft();
        _rootMenuContentDom.classList.add( 'u-hidden-overflow' );

        _activeMenu = _rootMenu;

        _suspended = false;
      }

      return !_suspended;
    }

    /**
     * Remove events necessary for the desktop menu behaviors.
     * @returns {boolean} Whether it has successfully been suspended or not.
     */
    function suspend() {
      if ( !_suspended ) {
        _suspended = true;

        _rootMenu.getTransition().remove();

        var rootNode = _menus.getRoot();
        treeTraversal.bfs( rootNode, function( node ) {
          node.data.setCollapseTransition( null );
          node.data.setExpandTransition( null );

          // TODO: Investigate whether deferred collapse has another solution.
          //       This check is necessary since a call to an already collapsed
          //       menu will set a deferred collapse that will be called
          //       on expandEnd next time the flyout is expanded.
          //       The deferred collapse is used in cases where the
          //       user clicks the flyout menu while it is animating open,
          //       so that it appears like they can collapse it, even when
          //       clicking during the expand animation.
          if ( node.data.isExpanded() ) {
            node.data.collapse();
          }
        } );

        _rootMenuContentDom.classList.remove( 'u-invisible' );
        _rootMenuContentDom.classList.remove( 'u-hidden-overflow' );

        // TODO: Investigate updating this to close the menus directly
        //       so `_handleCollapseEnd` is fired.
        this.dispatchEvent( 'rootCollapseEnd', { target: this } );
        _bodyDom.removeEventListener( 'mousedown', _handleBodyClick );
      }

      return _suspended;
    }

    // Attach public events.
    var eventObserver = new EventObserver();
    this.addEventListener = eventObserver.addEventListener;
    this.removeEventListener = eventObserver.removeEventListener;
    this.dispatchEvent = eventObserver.dispatchEvent;

    this.collapse = collapse;
    this.handleEvent = handleEvent;
    this.init = init;
    this.resume = resume;
    this.suspend = suspend;

    return this;
  }

  module.exports = MegaMenuMobile;


/***/ },
/* 33 */
/***/ function(module, exports) {

  'use strict';

  /**
   * Perform a backtrack up a Tree to the root.
   * Given this Tree and starting at (C):
   *
   *        R
   *       / \
   *      A   B
   *    / | \
   *   C  D  E
   *
   * Returns (C) -> (A) -> (R).
   *
   * @param {TreeNode} node - Node within a tree to traverse from.
   * @param {Function} callback - Function to call at each node.
   *   `this` will be the treeTranserval module within the callback.
   */
  function backtrack( node, callback ) {
    callback.call( this, node );
    var parent = node.parent;
    if ( parent ) {
      backtrack.apply( this, [ parent, callback ] );
    }
  }

  /**
   * Perform an iterative breadth-first search of a Tree.
   * Given this Tree and starting at (R):
   *
   *        R
   *       / \
   *      A   B
   *    / | \
   *   C  D  E
   *
   * Returns (R) -> (A) -> (B) -> (C) -> (D) -> (E).
   *
   * @param {TreeNode} node - Node within a tree to traverse from.
   * @param {Function} callback - Function to call at each node.
   *   `this` will be the treeTranserval module within the callback.
   */
  function bfs( node, callback ) {
    var queue = [ node ];
    var currNode;
    var children;
    while( queue.length > 0 ) {
      currNode = queue.shift();
      children = currNode.children;
      if ( children.length > 0 ) {
        queue = queue.concat( children );
      }
      callback.call( this, currNode );
    }
  }

  /**
   * Perform a recursive depth-first search of a Tree.
   * Given this Tree and starting at (R):
   *
   *        R
   *       / \
   *      A   B
   *    / | \
   *   C  D  E
   *
   * Returns (R) -> (A) -> (C) -> (D) -> (E) -> (B).
   *
   * @param {TreeNode} node - Node within a tree to traverse from.
   * @param {Function} callback - Function to call at each node.
   *   `this` will be the treeTranserval module within the callback.
   */
  function dfs( node, callback ) {
    callback.call( this, node );
    var children = node.children;
    for ( var i = 0, len = children.length; i < len; i++ ) {
      dfs.apply( this, [ children[i], callback ] );
    }
  }

  module.exports = {
    backtrack: backtrack,
    bfs:       bfs,
    dfs:       dfs
  };


/***/ },
/* 34 */
/***/ function(module, exports) {

  'use strict';

  /**
   * Tree
   * @class
   *
   * @classdesc A tree data structure.
   * Trees have one root node, and child nodes that branch.
   * Like:
   *
   *        R
   *       / \
   *      A   B
   *    / | \
   *   C  D  E
   *
   * @returns {Tree} An instance.
   */
  function Tree() {

    var _root = null;
    var _levelCache = {};

    /**
     * @param {Object} data - Data to attach to the root node.
     * @returns {Tree} An instance.
     */
    function init( data ) {
      _root = new TreeNode( this, data );
      _levelCache[0] = [ _root ];

      return this;
    }

    /**
     * @param {Object} data - Data to attach to new node.
     * @param {TreeNode} parent - Node on which to add a new child node.
     * @returns {TreeNode} The newly instantiated and added node.
     */
    function add( data, parent ) {
      var child = new TreeNode( this, data, parent );

      // Save node at each level as a flat array.
      var level = child.level;
      if ( _levelCache[level] ) {
        _levelCache[level].push( child );
      } else {
        _levelCache[level] = [ child ];
      }

      parent.children.push( child );

      return child;
    }

    /**
     * @returns {TreeNode} The root node of this Tree.
     */
    function getRoot() {
      return _root;
    }

    /**
     * Get all nodes at a particular tree level. For example, returning
     * Given this Tree and starting at (R):
     *
     *        R
     *       / \
     *      A   B
     *    / | \
     *   C  D  E
     *
     * Level 0 nodes would return (R).
     * Level 1 nodes would return (A) and (B).
     * Level 2 nodes would return (C), (D), and (E).
     *
     * @param {number} level - The tree level on which to return nodes.
     * @returns {Array} A list of all nodes at a particular tree level.
     */
    function getAllAtLevel( level ) {
      var levelCache = _levelCache[level];
      if ( !levelCache ) levelCache = [];
      return levelCache;
    }

    // TODO: Implement remove method.
    // function remove( child, parent ) {
    //
    // }

    this.add = add;
    this.init = init;
    this.getRoot = getRoot;
    this.getAllAtLevel = getAllAtLevel;

    return this;
  }

  // PRIVATE CLASS
  /**
   * TreeNode
   * @class
   *
   * @classdesc A node in a tree data structure.
   *
   * @param {Tree} tree - The data structure this node is a member of.
   * @param {Object} data - The data payload.
   * @param {TreeNode} parent - The parent node in the root,
   *   null if this is the root node.
   * @param {Arrray} children - List of children nodes.
   * @returns {TreeNode} An instance.
   */
  function TreeNode( tree, data, parent, children ) {
    this.tree = tree;
    this.data = data;
    this.parent = parent;
    this.children = children || [];
    this.level = parent ? parent.level + 1 : 0;

    return this;
  }

  module.exports = Tree;


/***/ }
/******/ ]);
