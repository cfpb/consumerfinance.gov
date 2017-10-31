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

    // Init cShowHide plugin
    $( '.show-hide' ).cShowHide();
});


$.fn.cShowHide = function cShowHide() {

    this.filter( '.default-hidden' ).find( '.show-hide-content' ).hide();

    this.find( '.show-hide-link' ).click( function( e ) {

        e.preventDefault();
        var $clicked_show_hide_a = $( this );

        // The entire SHow/Hide DOM object:
        var $show_hide = $( this ).parent( '.show-hide' );

        var $show_hide_content = $show_hide.find( '> .show-hide-content' );

        var textshow = escape($( this ).attr( 'data-textshow' ));

        var texthide = escape($( this ).attr( 'data-texthide' ));

        if ( $show_hide.hasClass( 'default-hidden' ) ) {
            $show_hide.removeClass( 'default-hidden' );
            $show_hide_content.slideDown( 500 );
            $clicked_show_hide_a.find( 'span' ).html( texthide );
        } else {
            $show_hide.addClass( 'default-hidden' );
            $show_hide_content.slideUp( 500 );
            $clicked_show_hide_a.find( 'span' ).html( textshow );
        }
    });
};

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
