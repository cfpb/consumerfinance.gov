/* ==========================================================================
   Scripts for /browse-filterable/.
   ========================================================================== */

'use strict';

// List of organisms used.
var Notification = require( '../../molecules/Notification' );
var FilterableListControls = require( '../../organisms/FilterableListControls' );

var notifications = document.querySelectorAll( '.m-notification' );
var notification;
for ( var i = 0, len = notifications.length; i < len; i++ ) {
	notification = new Notification( notifications[i] ).init();
}
var filterableListControls = new FilterableListControls( document.body ).init();
