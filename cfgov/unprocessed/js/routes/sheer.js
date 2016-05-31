/* ==========================================================================
   Common scripts that are used on old sheer templates
   These should be removed as templates are moved to wagtail
   ========================================================================== */

'use strict';

// List of modules often used.
var FilterableListControls = require( '../organisms/FilterableListControls' );
var Expandable = require( '../organisms/Expandable' );

var filterableListDom = document.querySelectorAll( '.o-filterable-list-controls' );
var filterableListControls;
if ( filterableListDom ) {
  for ( var i = 0, len = filterableListDom.length; i < len; i++ ) {
    filterableListControls = new FilterableListControls( filterableListDom[i] );
    filterableListControls.init();
  }
}

var expandableDom = document.querySelectorAll( '.content .o-expandable' );
var expandable;
if ( expandableDom ) {
  for ( var i = 0, len = expandableDom.length; i < len; i++ ) {
    expandable = new Expandable( expandableDom[i] );
    expandable.init();
  }
}
