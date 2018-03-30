import $ from 'jquery';

// Owning a Home - Loan Estimate custom analytics file

const OAHLEAnalytics = ( function() {

  const delay = ( function() {
    let timer = 0;
    return function( callback, ms ) {
      clearTimeout( timer );
      timer = setTimeout( callback, ms );
    };
  } )();

  $( '.tab-link' ).click( function() {
    const text = $( this ).text().trim();
    window.dataLayer.push( {
      event: 'OAH Loan Estimate Interaction',
      action: 'Tab click',
      label: text
    } );
  } );

  $( '.form-explainer_page-link ' ).click( function() {
    const pageNumber = 'Page ' + $( this ).attr( 'data-page' );
    window.dataLayer.push( {
      event: 'OAH Loan Estimate Interaction',
      action: 'Page link click',
      label: pageNumber
    } );
  } );

  $( '.form-explainer_page-buttons button' ).click( function() {
    let currentPage = 'Page ' + $( '.form-explainer_page-link.current-page' ).attr( 'data-page' ),
        action = 'Next Page button clicked';
    if ( $( this ).hasClass( 'prev' ) ) {
      action = 'Previous Page button clicked';
    }
    window.dataLayer.push( {
      event: 'OAH Loan Estimate Interaction',
      action: action,
      label: currentPage
    } );

  } );

  $( '.expandable_target' ).click( function() {
    let ele = $( this ),
        tab = ele.closest( '.explain' ).find( '.active-tab' ),
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
        window.dataLayer.push( {
          event: 'OAH Loan Estimate Interaction',
          action: action,
          label: text
        } );
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
        window.dataLayer.push( {
          event: 'OAH Loan Estimate Interaction',
          action: action,
          label: text
        } );
      }, 250 );
  } );


} )( $ );
