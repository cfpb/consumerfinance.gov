/* ==========================================================================
   View

   Backbone inspired lightweight MVC view.

   Code copied from the following with minimal modification :

   - Backbone.js ( http://backbonejs.org/docs/backbone.html ).
   ========================================================================== */

'use strict';

require( '../polyfill/function-bind' );
require( '../polyfill/event-listener' );

var _addClass = require( 'amp-add-class' );
var _assign = require( '../util/assign' );
var _extend = require( '../util/extend' );
var _isFunction = require( '../util/type-checkers' ).isFunction;
var _removeClass = require( 'amp-remove-class' );
var _result = require( '../util/result' );
var _uniqueId = require( 'lodash.uniqueid' );
var Delegate = require( 'dom-delegate' ).Delegate;
var Events = require( '../util/mixins/Events' );


var _delegateEventSplitter = /^(\S+)\s*(.*)$/;

function View( attrs ) {
  this.cid = _uniqueId( 'view' );
  attrs = attrs || ( attrs = {} );
  _assign( this, attrs, this.defaults );
  this.ensureElement();
  this.setCachedElements();
  this.initialize.apply( this, arguments );
}

// Public Methods and properties.

_assign( View.prototype, Events, {

  tagName: 'div',

  initialize: function initialize() {},

  render: function() {
    return this;
  },

  createElement: function( tagName ) {
    return document.createElement( tagName );
  },

  ensureElement: function() {
    if ( !this.el ) {
      var attrs = _assign( {}, _result( this, 'attributes' ) );
      if ( this.id ) attrs.id = _result( this, 'id' );
      if ( this.className ) attrs['class'] = _result( this, 'className' );
      this.setElement( this.createElement( _result( this, 'tagName' ) ) );
      this.setElementAttributes( attrs );
    } else {
      this.setElement( _result( this, 'el' ) );
    }
  },

  setElement: function( element ) {
    this.undelegateEvents();
    this.el = element;
    this.delegateEvents();

    return this;
  },

  setCachedElements: function( ) {
    var key;

    for ( key in this.cachedElements ) {
      if ( this.cachedElements.hasOwnProperty( key ) ) {
        this[key] = this.el.querySelector( this.cachedElements[key] );
      }
    }

    return this;
  },

  remove: function() {
    if ( this.el ) {
      this.el.parentNode.removeChild( this.el );
      if ( this.el.view ) delete this.el.view;
      delete this.el;
    }

    this.undelegateEvents();
    delete this;

    return true;
  },

  setElementAttributes: function( attributes ) {
    var property;
    for ( property in attributes ) {
      if ( attributes.hasOwnProperty( property ) ) {
        this.el.setAttribute( property, attributes[property] );
      }
    }
  },

  css: function( property, value ) {
    this.el.style[property] = value;
  },

  addClass: function( className, el ) {
    _addClass( el || this.el, className );

    return this;
  },

  removeClass: function( className, el ) {
    _removeClass( el || this.el, className );

    return this;
  },

  delegateEvents: function( events ) {
    var key;
    var method;
    var match;
    events = events || ( events = this.events );
    if ( !events ) return this;
    this.undelegateEvents();
    this._delegate = new Delegate( this.el );
    for ( key in events ) {
      method = events[key];
      if ( _isFunction( this[method] ) ) method = this[method];
      if ( !method ) continue;
      match = key.match( _delegateEventSplitter );
      this.delegate( match[1], match[2], method.bind( this ) );
    }

    return this;
  },

  delegate: function( eventName, selector, listener ) {
    this._delegate.on( eventName, selector, listener );

    return this;
  },

  undelegateEvents: function() {
    if ( this._delegate ) {
      this._delegate.destroy();
    }
    return this;
  }

} );


// Static Methods

View.extend = _extend;

View.getInstance = function getViewInstance( selector ) {
  var _element = document.querySelectorAll( selector )[0];
  var _isDefined = typeof _element !== 'undefined' &&
                  _element.hasOwnProperty( 'view' );
  var _isInstance = _isDefined && _element.view instanceof View;

  return _isInstance && _element.view || window.undefined;
};

View.init = function init() {
  var _elements = document.querySelectorAll( this.selector );
  var _element;
  var _view;

  for ( var i = 0; i < _elements.length; ++i ) {
    _element = _elements[i];
    _view = new this( { el: _element } );
    _element.view = _view;
  }

  return this;
};

module.exports = View;
