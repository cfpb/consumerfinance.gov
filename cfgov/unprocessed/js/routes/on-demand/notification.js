/* ==========================================================================
   Scripts for Notification Molecule.
   ========================================================================== */

'use strict';

var Notification = require( '../../molecules/Notification' );

var notifications = document.querySelectorAll( '.m-notification' );
var notification;
for ( var i = 0, len = notifications.length; i < len; i++ ) {
	notification = new Notification( notifications[i] ).init();
}

