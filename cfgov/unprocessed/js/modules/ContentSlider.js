'use strict';

var $ = require( 'jquery' );
require( 'slick' );

var EventObserver = require( '../modules/util/EventObserver' );
var fnBind = require( '../modules/util/fn-bind' ).fnBind;

/**
 * ContentSlider
 * @class
 *
 * @classdesc Slides content in and out of a container div.
 *
 * When an element inside container with class `content-show`
 * is clicked, the element matching its `data-content` value
 * will be cloned, inserted in a slide, and rotated into view in the
 * container, whose height will be recalculated to match new contents.
 * When elements with class `content-hide` are clicked,
 * the slide containing the element will be rotated out of view
 * and then removed from the DOM.
 *
 * @param {string} elem - Container element.
 * @returns {ContentSlider} An instance.
 */
function ContentSlider( elem ) {

  // Constants.
  /**
   * @constant
   * @type {number}
   * @description
   *  Carousel transition speed in milliseconds.
   */
  var SPEED = 300;

  var _$container = $( elem );

  var _slideCount = 0;
  var _slickObj;

  /**
   * @param {number} numSlides - Number of permanent slides in the container.
   * @returns {ContentSlider} An instance.
   */
  function init( numSlides ) {
    _slideCount = numSlides;

    // Initialize slick carousel.
    var slickOpts = {
      dots:           false,
      infinite:       false,
      swipe:          false,
      speed:          SPEED,
      adaptiveHeight: true,
      arrows:         false
    };

    _$container.on( 'afterChange', fnBind( _afterChangeHandler, this ) );
    _$container.on( 'beforeChange', _beforeChangeHandler );
    _$container.on( 'init', fnBind( _initHandler, this ) );
    _$container.slick( slickOpts );

    return this;
  }

  /**
   * @param {Object} event - Slick event.
   * @param {Object} slider - Reference to the slick slider instance.
   */
  function _initHandler( event, slider ) {
    _slickObj = slider;
    _$container.height( $( _slickObj.$slides[0] ).height() );

    // Set up events.
    _$container.on(
      'click.slider',
      '.content-show',
      $.proxy( _slideInContent, this )
    );
    _$container.on(
      'click.slider',
      '.content-hide',
      $.proxy( _slideOutContent, this )
    );

    // Overwrite the default method to set height
    // There are performance implications of doing so
    // as noted here https://github.com/kenwheeler/slick/issues/83.
    // ( Although wildly exaggerated. )
    _slickObj.setHeight = function setHeight() {
      this.$list.css( 'height', 'auto' );
    };
  }

  /**
   * @param {Object} event - Slick event.
   * @param {Object} slider - Reference to the slick slider instance.
   * @param {number} currInd - Current slide number.
   * @param {number} targetInd - Slide number to switch to.
   */
  function _afterChangeHandler( event, slider, currInd, targetInd ) {
    // Init the Expandable after the nodes have been cloned.
    this.dispatchEvent( 'afterChange', {
      target: this, currInd: currInd, targetInd: targetInd
    } );
  }

  /**
   * @param {Object} event - Slick event.
   * @param {Object} slider - Reference to the slick slider instance.
   * @param {number} currInd - Current slide number.
   * @param {number} targetInd - Slide number to switch to.
   */
  function _beforeChangeHandler( event, slider, currInd, targetInd ) {
    // When slide is changed,
    // animate height of container to accommodate new slide's height.
    var slide = slider.$slides[targetInd];
    slider.$slider.animate(
      { height: $( slide ).height() + 'px' }, SPEED
    );
  }

  /**
   * @param {Object} event - click.slider event.
   */
  function _slideInContent( event ) {
    event.preventDefault();
    var $div = $( '<div>' );
    var $node = $( $( event.currentTarget ).data( 'content' ) );
    if ( $node.length ) {
      // TODO: Move content instead of cloning; use ids instead of classes.
      $node.first().clone().show().appendTo( $div );
      _$container.slick( 'slickAdd', $div );
      _$container.slick( 'slickNext' );
    }
  }

  /**
   * @param {Object} event - click.slider event.
   */
  function _slideOutContent( event ) {
    event.preventDefault();
    _$container.slick( 'slickPrev' );

    // Once slide has been animated out of view, remove it from DOM.
    setTimeout( function() {
      _$container.slick( 'slickRemove', _slickObj.$slides.length - 1 );
    }, SPEED );
  }

  /**
   * @returns {ContentSlider} An instance.
   */
  function destroy() {

    // Remove all but permanent slides.
    while ( _slickObj.$slides.length > _slideCount ) {
      _$container.slick( 'slickRemove', _slickObj.$slides.length - 1 );
    }

    // Remove listeners on container.
    _$container.off( 'click.slider' );
    _$container.slick( 'unslick' );

    return this;
  }

  /**
   * Sets container to height: auto.
   * @returns {ContentSlider} An instance.
   */
  function setHeightToAuto() {
    _$container.height( 'auto' );

    return this;
  }

  // Export public methods.
  var eventObserver = new EventObserver();
  this.addEventListener = eventObserver.addEventListener;
  this.removeEventListener = eventObserver.removeEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;

  this.init = init;
  this.destroy = destroy;
  this.setHeightToAuto = setHeightToAuto;

  return this;
}

module.exports = ContentSlider;
