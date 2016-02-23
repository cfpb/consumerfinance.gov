/* ==========================================================================
   Scripts for /browse-filterable/.
   ========================================================================== */

'use strict';

// List of organisms used.
var SecondaryNavigation = require( '../../organisms/SecondaryNavigation' );
var Notification = require( '../../molecules/Notification' );
var FilterableListControls = require( '../../organisms/FilterableListControls' );

var secondaryNavigation = new SecondaryNavigation( document.body ).init();

var notifications = document.querySelectorAll( '.m-notification' );
var notification;
for ( var i = 0, len = notifications.length; i < len; i++ ) {
	notification = new Notification( notifications[i] ).init();
}
