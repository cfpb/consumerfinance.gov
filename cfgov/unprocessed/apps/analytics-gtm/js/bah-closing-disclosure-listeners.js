// TODO: Remove $.
import $ from 'jquery';

import {
  delay,
  track
} from './util/analytics-util';

const OAHCDAnalytics = ( function( $ ) {

  $( '.tab-link' ).click( function() {
    const text = $( this ).text().trim();
    track( 'OAH Closing Disclosure Interaction', 'Tab click', text );
  } );

  $( '.form-explainer_page-link' ).click( function() {
    const pageNumber = 'Page ' + $( this ).attr( 'data-page' );
    track(
      'OAH Closing Disclosure Interaction', 'Page link click', pageNumber
    );
  } );

  $( '.form-explainer_page-buttons button' ).click( function() {
    const currentPage = 'Page ' + $( '.form-explainer_page-link.current-page' ).attr( 'data-page' );
    let action = 'Next Page button clicked';
    if ( $( this ).hasClass( 'prev' ) ) {
      action = 'Previous Page button clicked';
    }
    track( 'OAH Closing Disclosure Interaction', action, currentPage );

  } );

  $( '.o-expandable_target' ).click( function() {
    const ele = $( this );
    const tab = $( this ).closest( '.explain' ).find( '.active-tab' );
    const tabText = tab.find( '.tab-label' ).text().trim();
    delay(
      function() {
        const state = ele.attr( 'aria-pressed' );
        let action = 'Expandable collapsed - ' + tabText;
        const label = $( '<p>' + ele.find( '.o-expandable_label' ).html() + '</p>' );
        let text = '';

        label.find( 'span' ).empty();
        text = label.text().trim();

        if ( state === 'true' ) {
          action = 'Expandable expanded - ' + tabText;
        }
        track( 'OAH Closing Disclosure Interaction', action, text );
      }, 250 );
  } );

  $( '.image-map_overlay' ).click( function() {
    const href = $( this ).attr( 'href' );
    const text = $( this ).text().trim();
    delay(
      function() {
        let action = 'Image Overlay click - expandable collapsed';
        const target = $( href );
        if ( target.hasClass( 'o-expandable__expanded' ) ) {
          action = 'Image Overlay click - expandable expanded';
        }
        track( 'OAH Closing Disclosure Interaction', action, text );
      }, 250 );
  } );

} )( $ );
