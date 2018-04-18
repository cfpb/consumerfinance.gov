// TODO: Remove jquery.
import $ from 'jquery';

import {
  addEventListenerToElem,
  delay,
  track
} from './util/analytics-util';

// Owning a Home - Loan Estimate custom analytics file

const OAHLEAnalytics = ( function() {

  $( '.tab-link' ).click( function() {
    const text = $( this ).text().trim();
    track( 'OAH Loan Estimate Interaction', 'Tab click', text );
  } );

  $( '.form-explainer_page-link ' ).click( function() {
    const pageNumber = 'Page ' + $( this ).attr( 'data-page' );
    track( 'OAH Loan Estimate Interaction', 'Page link click', pageNumber );
  } );

  $( '.form-explainer_page-buttons button' ).click( function() {
    let currentPage = 'Page ' + $( '.form-explainer_page-link.current-page' ).attr( 'data-page' ),
        action = 'Next Page button clicked';
    if ( $( this ).hasClass( 'prev' ) ) {
      action = 'Previous Page button clicked';
    }
    track( 'OAH Loan Estimate Interaction', action, currentPage );
  } );

  $( '.o-expandable_target' ).click( function() {
    let ele = $( this ),
        tab = ele.closest( '.explain' ).find( '.active-tab' ),
        tabText = tab.find( '.tab-label' ).text().trim();
    delay(
      function() {
        let state = ele.attr( 'aria-pressed' ),
            action = 'Expandable collapsed - ' + tabText,
            label = $( '<p>' + ele.find( '.o-expandable_label' ).html() + '</p>' ),
            text = '';

        label.find( 'span' ).empty();
        text = label.text().trim();

        if ( state === 'true' ) {
          action = 'Expandable expanded - ' + tabText;
        }
        track( 'OAH Loan Estimate Interaction', action, text );
      }, 250 );
  } );

  $( '.image-map_overlay' ).click( function() {
    let href = $( this ).attr( 'href' ),
        text = $( this ).text().trim();
    delay(
      function() {
        let action = 'Image Overlay click - expandable collapsed',
            target = $( href );
        if ( target.hasClass( 'o-expandable__expanded' ) ) {
          action = 'Image Overlay click - expandable expanded';
        }
        track( 'OAH Loan Estimate Interaction', action, text );
      }, 250 );
  } );

} )( $ );
