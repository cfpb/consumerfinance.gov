/* ==========================================================================
   Base Video Player Class
   ========================================================================== */

import { assign } from './util/assign';
import { noopFunct } from './util/standard-type';
import * as jsLoader from './util/js-loader';

import ERROR_MESSAGES from '../config/error-messages-config';

const DOM_INVALID = ERROR_MESSAGES.DOM.INVALID;

const CLASSES = Object.freeze( {
  VIDEO_PLAYER_SELECTOR:     '.video-player',
  VIDEO_PLAYING_STATE:       'video-playing',
  IMAGE_SELECTOR:            '.video-player_image',
  IFRAME_CLASS_NAME:         'video-player_iframe',
  IFRAME_CONTAINER_SELECTOR: '.video-player_iframe-container',
  PLAY_BTN_SELECTOR:         '.video-player_play-btn',
  CLOSE_BTN_SELECTOR:        '.video-player_close-btn'
} );


// Private properties.
let _isIframeLoaded = false;
let _isIframeLoading = false;
let _isVideoPlaying = false;
let _isVideoStopped = true;
let _this;

/**
 * VideoPlayer
 * @class
 *
 * @classdesc Base Video Player class.
 * @param {HTMLNode} element - The DOM element to use as the base element.
 * @param {Object} options - attributes used to extend the video player
 */
function VideoPlayer( element, options ) {
  _this = this;
  options = options || {};
  this.baseElement = _ensureElement( element, options.createIFrame );
  this.iFrameProperties = assign(
    {},
    this.baseElement.dataset,
    this.iFrameProperties
  );

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
  assign( child.prototype, attributes );
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
  const videoPlayerElement = document.querySelector( selector );

  // Nothing to initialize
  if ( !videoPlayerElement ) return;

  const videoPlayer = new this( videoPlayerElement );

  _attachIFrame();

  /* eslint-disable consistent-return */
  return videoPlayer;
};

// Private Methods.

// TODO Fix complexity issue
/* eslint-disable complexity */
/**
 * Function used to attach the video iframe.
 * @throws Will throw an error if no iframe element is found.
 * @returns {HTMLNode} A dom element.
 */
function _attachIFrame() {
  let iFrameElement = _this.childElements.iFrame;
  const iFrameContainerElement = _this.childElements.iFrameContainer;

  if ( _isIframeLoaded === false && _isIframeLoading === false &&
    iFrameElement === null ) {
    iFrameElement = _createElement( 'iframe', _this.iFrameProperties );
    iFrameElement.classList.add( CLASSES.IFRAME_CLASS_NAME );
    iFrameElement.setAttribute( 'frameborder', 0 );
    _this.state.isIframeLoading = true;
    iFrameElement.onload = function onload() {
      _this.state.setIsIframeLoaded( true );
    };
    iFrameContainerElement.appendChild( iFrameElement );
  } else if ( _this.childElements.iframeContainer === null ) {
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
  const createdElement = document.createElement( tagName );
  let property;
  const hasOwnProperty = Object.hasOwnProperty.bind( properties );

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
  if ( domElement instanceof HTMLElement === false ) {
    msg = msg || DOM_INVALID;
    throw new Error( msg );
  }

  return domElement;
}

/**
 * Function used to initialize events.
 */
function _initEvents() {
  const playAction = _onAction.bind( _this, 'play' );
  const stopAction = _onAction.bind( _this, 'stop' );

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
  let elementName;
  const hasOwnProperty = Object.hasOwnProperty.bind( _this.childElements );
  const querySelector = _this.baseElement.querySelector
    .bind( _this.baseElement );

  for ( elementName in elements ) {
    if ( hasOwnProperty( elementName ) ) {
      elements[elementName] = querySelector( elements[elementName] );
    }
  }

  return elements;
}


// Public methods.

const API = {

  baseElement: null,

  childElements: {
    image:           CLASSES.IMAGE_SELECTOR,
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
    jsLoader.loadScript( script || this.SCRIPT_API, callback || onScriptLoad );
  },

  init: noopFunct,

  iFrameProperties: {
    allowfullscreen: 'true',
    scrolling:       'no',
    src:             '',
    width:           '100%'
  },

  state: {
    isIframeLoading: false,
    isPlayerInitialized: false,
    isScriptLoading: false,
    getIsIframeLoaded: function() {
      return _isIframeLoaded;
    },
    setIsIframeLoaded: function( value ) {
      if ( value === true ) _isIframeLoading = false;
      _isIframeLoaded = value;
    },
    getIsVideoPlaying: function() {
      return _isVideoPlaying;
    },
    setIsVideoPlaying: function( value ) {
      if ( value === true ) _isVideoStopped = false;
      _isVideoPlaying = value;
    },
    getIsVideoStopped: function() {
      return _isVideoStopped;
    },
    setIsVideoStopped: function( value ) {
      if ( value === true ) _isVideoPlaying = false;
      _isVideoStopped = value;
    }
  },

  /**
   * Function used to play the video player.
   */
  play: function play( ) {
    this.baseElement.classList.add( CLASSES.VIDEO_PLAYING_STATE );
    this.state.setIsVideoPlaying( true );
  },

  /**
   * Function used to stop the video player.
   */
  stop: function stop( ) {
    this.baseElement.classList.remove( CLASSES.VIDEO_PLAYING_STATE );
    this.state.setIsVideoStopped( true );
  }
};

assign( VideoPlayer.prototype, API );

// Expose public methods.
export default VideoPlayer;
