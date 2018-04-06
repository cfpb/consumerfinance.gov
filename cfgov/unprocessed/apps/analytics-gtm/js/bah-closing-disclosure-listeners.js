// TODO: Remove $.
import $ from '$';

import {
  delay,
  track
} from './util/analytics-util';

const OAHCDAnalytics = ( function( $ ) {

  $( '.tab-link' ).click( function() {
    const text = $( this ).text().trim();
    track( 'OAH Closing Disclosure Interaction', 'Tab click', text );
  } );

  $( '.form-explainer_page-link ' ).click( function() {
    const pageNumber = 'Page ' + $( this ).attr( 'data-page' );
    track(
      'OAH Closing Disclosure Interaction', 'Page link click', pageNumber
    );
  } );

  $( '.form-explainer_page-buttons button' ).click( function() {
    let currentPage = 'Page ' + $( '.form-explainer_page-link.current-page' ).attr( 'data-page' ),
        action = 'Next Page button clicked';
    if ( $( this ).hasClass( 'prev' ) ) {
      action = 'Previous Page button clicked';
    }
    track( 'OAH Closing Disclosure Interaction', action, currentPage );

  } );

  $( '.expandable_target' ).click( function() {
    let ele = $( this ),
        tab = $( this ).closest( '.explain' ).find( '.active-tab' ),
        tabText = tab.find( '.tab-label' ).text().trim();
    delay(
      function() {
        let state = ele.attr( 'aria-pressed' ),
            action = 'Expandable collapsed - ' + tabText,
            label = $( '<p>' + ele.find( '.expandable_label' ).html() + '</p>' ),
            text = '';

        label.find( 'span' ).empty();
        text = label.text().trim();

        if ( state === 'true' ) {
          action = 'Expandable expanded - ' + tabText;
        }
        track( 'OAH Closing Disclosure Interaction', action, text );
      }, 250 );
  } );

  $( '.image-map_overlay' ).click( function() {
    let href = $( this ).attr( 'href' ),
        text = $( this ).text().trim();
    delay(
      function() {
        let action = 'Image Overlay click - expandable collapsed',
            target = $( href );
        if ( target.hasClass( 'expandable__expanded' ) ) {
          action = 'Image Overlay click - expandable expanded';
        }
        track( 'OAH Closing Disclosure Interaction', action, text );
      }, 250 );
  } );

} )( $ );
