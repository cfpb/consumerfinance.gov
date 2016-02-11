/* ==========================================================================
   Scripts for /browse-filterable/.
   ========================================================================== */

'use strict';

// List of organisms used.
var Notification = require( '../../molecules/Notification' );
var FilterableListControls = require( '../../organisms/FilterableListControls' );
var Multiselect = require( '../../molecules/Multiselect' );

var notifications = document.querySelectorAll( '.m-notification' );
var notification;
for ( var i = 0, len = notifications.length; i < len; i++ ) {
	notification = new Notification( notifications[i] ).init();
}
var filterableListControls = new FilterableListControls( document.body ).init();
var multiselect = new Multiselect( document.querySelector( 'select[multiple]' ) );
multiselect.init();
