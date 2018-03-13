'use strict';

var $ = require( 'jquery' );

$( '.tab-link' ).click( function( evt ) {
  var $tabs = $( '.tab-list' ),
      $tabLi = $( this ).parent( '.tab-list' ),
      $tabContent = $( '.tab-content' ),
      current = $( this ).attr( 'href' );

  $tabs.removeClass( 'active-tab' );
  $tabLi.addClass( 'active-tab' );

  $tabContent.hide();
  $( current ).show();

  evt.preventDefault();

} );
