/* ==========================================================================
    Base Video Player Class
   ========================================================================== */

'use strict';

var _assign = require( './util/assign' ).assign;
var _noopFunct = require( './util/standard-type' ).noopFunct;
var _jsLoader = require( './util/js-loader' );
var _dataSet = require( './util/data-set' ).dataSet;

var DOM_INVALID = require( '../config/error-messages-config' ).DOM.INVALID;

var CLASSES = Object.freeze( {
  VIDEO_PLAYER_SELECTOR:     '.video-player',
  VIDEO_PLAYING_STATE:       'video-playing',
  IFRAME_CLASS_NAME:         'video-player_iframe',
  IFRAME_CONTAINER_SELECTOR: '.video-player_iframe-container',
  PLAY_BTN_SELECTOR:         '.video-player_play-btn',
  CLOSE_BTN_SELECTOR:        '.video-player_close-btn'
} );


// PRIVATE properties.
var _isIframeLoaded;
var _isIframeLoading;
var _isVideoPlaying;
var _isVideoStopped;
var _this;

/**
 * VideoPlayer
 * @class
 *
 * @classdesc Base Video Player class.
 * @param {HTMLNode} element - The DOM element to use as the base element.
 * @param {object} options - attributes used to extend the video player
 */
function VideoPlayer( element, options ) {
  _this = this;
  options = options || {};
  this.baseElement = _ensureElement( element, options.createIFrame );

  // TODO: Add utility function for dataset. Oh dear IE, how I love you.
  this.iFrameProperties = _assign( _dataSet( this.baseElement ) ||
    {}, this.iFrameProperties );

  _setChildElements( this.childElements );
  _initEvents();
  this.init.apply( this, arguments );
}

// Static Methods

/**
* Function used to extend Base Video Player class.
* @param {object} attributes - attributes assigned to a prototype.
* @returns {VideoPlayer} A class.
*/
VideoPlayer.extend = function extend( attributes ) {

  /**
  * Function used to create child Video Player class.
  * @returns {VideoPlayer} An instance.
  */
  function child() {
    this._super = VideoPlayer.prototype;
    return VideoPlayer.apply( this, arguments );
  }
  child.prototype = Object.create( VideoPlayer.prototype );
  _assign( child.prototype, attributes );
  child.init = VideoPlayer.init;

  return child;
};

/**
* Static method used to initialize class.
* @param {string} selector - attributes assigned to a prototype.
* @returns {VideoPlayer} An instance.
*/
VideoPlayer.init = function init( selector ) {
  selector = selector ||
  '[class*="=' + CLASSES.VIDEO_PLAYER_SELECTOR + '"]:' +
  'not([class*="' + CLASSES.VIDEO_PLAYER_SELECTOR + '"__"])';

  // There should only be one video player on the page.
  var videoPlayer;
  var videoPlayerElement = document.querySelector( selector );
  if ( videoPlayerElement ) {
    videoPlayer = new this( videoPlayerElement );
  }

  return videoPlayer;
};

// Private Methods.

/**
* Function used to attach the video iframe.
* @throws Will throw an error if no iframe element is found.
* @returns {HTMLNode} A dom element.
*/
function _attachIFrame() {
  var iFrameElement = _this.childElements.iFrame;
  var iFrameContainerElement = _this.childElements.iFrameContainer;
  var state = _this.state;

  if ( state.isIframeLoaded === false && state.isIframeLoading === false &&
    iFrameElement === null ) {
    iFrameElement = _createElement( 'iframe', _this.iFrameProperties );
    iFrameElement.classList.add( CLASSES.IFRAME_CLASS_NAME );
    iFrameElement.setAttribute( 'frameborder', 0 );
    state.isIframeLoading = true;
    iFrameElement.onload =
      function oniFrameLoad() { state.isIframeLoaded = true; };
    iFrameContainerElement.appendChild( iFrameElement );
  } else if( _this.childElements.iframeContainer === null ) {
    throw new Error( 'No iframe container element found.' );
  }

  return iFrameElement;
}

/**
* Function used to create a dom element.
* @param {string} tagName - name of the type of dom element to create.
* @param {obect} properties - attributes used to assign to the element.
* @returns {HTMLNode} A dom element.
*/
function _createElement( tagName, properties ) {
  var createdElement = document.createElement( tagName );
  var property;
  var hasOwnProperty = Object.hasOwnProperty.bind( properties );

  for ( property in properties || {} ) {
    if ( hasOwnProperty( property ) ) {
      createdElement.setAttribute( property, properties[property] );
    }
  }

  return createdElement;
}

/**
* Function used to create a dom element.
* @param {HTMLNode} domElement - dom selector
* @param {string} msg - used for Error display.
* @returns {HTMLNode} A dom element.
*/
function _ensureElement( domElement, msg ) {
  if( domElement instanceof HTMLElement === false ) {
    msg = msg || DOM_INVALID;
    throw new Error( msg );
  }

  return domElement;
}

/**
* Function used to initialize events.
*/
function _initEvents() {
  var playAction = _onAction.bind( _this, 'play' );
  var stopAction = _onAction.bind( _this, 'stop' );

  _this.childElements.playBtn.addEventListener( 'click', playAction );
  _this.childElements.closeBtn.addEventListener( 'click', stopAction );
}

/**
* Function used to handle video player actions.
* @param {string} actionType - name of instance method.
* @param {Event} event - dom event.
*/
function _onAction( actionType, event ) {
  event.preventDefault();
  event.stopPropagation();
  if ( typeof this[actionType] === 'function' ) _this[actionType]();
}

/**
* Function used to set cached child elements.
* @param {object} elements - object with child element names.
* @returns {HTMLNode} An array of dom elements.
*/
function _setChildElements( elements ) {
  var elementName;
  var hasOwnProperty = Object.hasOwnProperty.bind( _this.childElements );
  var querySelector = _this.baseElement.querySelector
    .bind( _this.baseElement );

  for ( elementName in elements ) {
    if ( hasOwnProperty( elementName ) ) {
      elements[elementName] = querySelector( elements[elementName] );
    }
  }

  return elements;
}


// Public methods.

var API = {

  baseElement: null,

  childElements: {
    iFrame:          CLASSES.IFRAME_SELECTOR,
    iFrameContainer: CLASSES.IFRAME_CONTAINER_SELECTOR,
    playBtn:         CLASSES.PLAY_BTN_SELECTOR,
    closeBtn:        CLASSES.CLOSE_BTN_SELECTOR
  },

  /**
  * Function used to set cached child elements.
  */
  destroy: function destroy() {
    this.childElements.playBtn.removeEventListener( 'click', this.play );
    this.childElements.closeBtn.removeEventListener( 'click', this.stop );
  },

  /**
  * Function used to embed a script.
  * @param {string} script - url of script to load.
  * @param {function} callback - function called when script is loaded.
  */
  embedScript: function embedScript( script, callback ) {
    /**
    * Function called when script is loaded.
    */
    function onScriptLoad() { _this.state.isScriptLoading = false; }
    this.state.isScriptLoading = true;
    _jsLoader.loadScript( script || this.SCRIPT_API, callback || onScriptLoad );
  },

  init: _noopFunct,

  iFrameProperties: {
    allowfullscreen: 'true',
    scrolling:       'no',
    src:             '',
    width:           '100%'
  },
  // TODO: With this amount of states it probably makes more sense to have
  // getState/setState methods.
  state: {
    isIframeLoading: false,
    isPlayerInitialized: false,
    isScriptLoading: false,
    get isIframeLoaded() {
      return _isIframeLoaded || false;
    },
    set isIframeLoaded( value ) {
      if ( value === true ) _isIframeLoading = false;
      _isIframeLoaded = value;
    },
    get isVideoPlaying() {
      return _isVideoPlaying || false;
    },
    set isVideoPlaying( value ) {
      if ( value === true ) _isVideoStopped = false;
      _isVideoPlaying = value;
    },
    get isVideoStopped() {
      return _isVideoStopped || true;
    },
    set isVideoStopped( value ) {
      if ( value === true ) _isVideoPlaying = false;
      _isVideoStopped = value;
    }
  },

  /**
  * Function used to play the video player.
  */
  play: function play( ) {
    if( this.state.isIframeLoaded === false ) {
      _attachIFrame();
    }
    this.baseElement.classList.add( CLASSES.VIDEO_PLAYING_STATE );
    this.state.isVideoPlaying = true;
  },

  /**
  * Function used to stop the video player.
  */
  stop: function stop( ) {
    this.baseElement.classList.remove( CLASSES.VIDEO_PLAYING_STATE );
    this.state.isVideoStopped = true;
  }
};

_assign( VideoPlayer.prototype, API );

// Expose public methods.
module.exports = VideoPlayer;
