/* ==========================================================================
   Common scripts that are used on old sheer templates
   These should be removed as templates are moved to wagtail
   ========================================================================== */

'use strict';

// List of modules often used.
var FilterableListControls = require( '../organisms/FilterableListControls' );
var Expandable = require( '../molecules/Expandable' );

var filterableListDom = document.querySelector( '.o-filterable-list-controls' );
var filterableListControls;
if ( filterableListDom ) {
  for ( var i = 0, len = filterableListDom.length; i < len; i++ ) {
    filterableListControls = new FilterableListControls( document.body )
    filterableListControls.init();
  }
}
