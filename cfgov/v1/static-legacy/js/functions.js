// Trigger when page is ready.
$( document ).ready( function() {

    // Remove styles from feature images.
    $( 'a > img' ).each( function() {
        $( this ).parent().addClass( 'noStyles' );
    });

    // Add pdf class to pdf links.
    $( 'a[href$="pdf"]' ).each( function() {
        $( this ).addClass( 'pdf' );
    });

    // Stripe table rows in older browsers
    // if jquery is running and IE < 9.
    if (typeof $ !== 'undefined' && typeof is_lt_IE9 !== 'undefined') {
        $( 'table tbody tr:even' ).addClass( 'even' );
        $( 'table tbody tr:odd' ).addClass( 'odd' );
    }

    // Report specific js for sticky nav
    $(window).scroll( stickyNav );
});


function stickyNav() {
  $( '.report header h2' ).each( function() {
      var scrtop = $( window ).scrollTop();
      var positioner = $( this ).parent().parent();
      var offset = positioner.offset();
      offset.bottom = positioner.height() + offset.top;
      var id = positioner.attr( 'id' );
      section_link = $( '#nav-list' ).find( 'a[href="#' + id + '"]' );
      if ( ( offset.top <= scrtop ) && ( offset.bottom > scrtop ) ) {
          section_link.css( 'color', '#010101' );
      } else {
          section_link.css( 'color', '' );
      }
  });
}
