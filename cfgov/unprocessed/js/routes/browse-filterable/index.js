/* ==========================================================================
   Scripts for /browse-filterable/.
   ========================================================================== */

'use strict';

// List of organisms used.
const SecondaryNavigation = require( '../../organisms/SecondaryNavigation' );
const Notification = require( '../../molecules/Notification' );
const FilterableListControls = require( '../../organisms/FilterableListControls' );

const secondaryNavigation = new SecondaryNavigation( document.body ).init();

const notifications = document.querySelectorAll( '.m-notification' );
let notification;
for ( let i = 0, len = notifications.length; i < len; i++ ) {
	notification = new Notification( notifications[i] ).init();
}
