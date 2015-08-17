'use strict';

var View = require( '../classes/View' );

// TODO Find a smaller animation lib or roll simple lib.
var _animate = require( 'velocity-animate' );

var ExpandableView = View.extend( {

  // View Specific Properits / Methods

  events: {
    'click .expandable_target': 'toggle',
    'click .cueOpen':           'expand',
    'click .cueClose':          'collapse'
  },

  cachedElements: {
    content: '.expandable_content'
  },

  template: require( './expandableTemplate.hbs' ),

  // Custom default Properties

  defaults: {
    animationDuration: 500,
    isAccordian:       false,
    expanded:          false,
    expandClass:       'expandable__expanded'
  },

  // Custom Methods

  constrainValue: require( '../util/constrain-value' ),

  toggle: function() {
    if ( this.expanded ) {
      this.collapse();
    } else {
      this.expand();
    }
    this.trigger( 'toggle', this.expanded );

    return this;
  },

  expand: function( duration ) {
    this.addClass( this.expandClass, this.el );
    this.animate( duration, 'slideDown', this.content );
    this.expanded = true;

    return this;
  },

  collapse: function( duration ) {
    this.removeClass( this.expandClass, this.el );
    this.animate( duration, 'slideUp', this.content );
    this.expanded = false;

    return this;
  },

  animate: function( duration, animation, el ) {
    if ( duration !== 0 ) {
      duration = this.constrainValue( duration ) || this.animationDuration;
      _animate( el, animation, { duration: duration } );
    }
  }

} );

ExpandableView.selector = '.expandable';

module.exports = ExpandableView;
