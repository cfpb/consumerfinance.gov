const jQuery = require( 'jquery' );

/* 	This script uses a local Django API to acquire a list of the 10 closest
HUD Counselors by zip code. See hud_api_replace for more details on the
API queries. -wernerc */

/*	This class represents a namespace of functions that should be exposed
for testing purposes. */
var cfpb_hud_hca = ( function() {
  /*	check_zip() is an easy, useful function that takes a string and returns a valid zip code, or returns false.
  NOTE: 'Valid' means 5 numeric characters, not necessarily 'existant' and 'actually addressable.' */
  var check_zip = function( zip ) {
    if ( ( zip === null ) || ( zip === undefined ) || ( zip === false ) ) {
      return false;
    }
    else {
      zip = zip.toString().replace( /[^0-9]+/g,'' );
      zip = zip.slice(0,5);
      if ( zip.length === 5 ) {
        return zip;
      }
      else {
        return false;
      }
    }
  }

  /*	check_data_structure() just makes sure your data has the correct structure before you start
  requesting properties that don't exist in generate_html() and update_map() */
  var check_hud_data = function( data ) {
    if ( ( data === null ) || ( data === 0 ) || ( data === undefined ) ) {
      return false;
    }
    else if ( data.hasOwnProperty( 'error' ) ) {
      return 'error';
    }
    else if ( !( data.hasOwnProperty( 'counseling_agencies' ) ) ) {
      return false;
    }
    else if ( !( data.hasOwnProperty( 'zip' ) ) ) {
      return false;
    }
    else {
      return true;
    }
  }

  return {
    check_zip: check_zip,
    check_hud_data: check_hud_data
  }
}() );

(function($, L) { // start jQuery capsule

  var map;
  var marker_array = [];
  var zip_marker = null;


  /*	get_url_zip() is a simple function to retrieve the zip variable from the URL */
  function get_url_zip() {
    var zip = '';
    var keyvals = window.location.href.slice( window.location.href.indexOf( '?' ) + 1 ).split( '&' );
    $.each( keyvals , function( i, val ) {
      var parts = val.split( '=' );
      if ( parts[0] == 'zip' ) {
        zip = parts[1];
      }
    } );
    return ( cfpb_hud_hca.check_zip( zip ) );
  }

  /*	initialize_map() sets options and creates the map */
  function initialize_map() {
    L.mapbox.accessToken = mapbox_access_token,
    map = L.mapbox.map( 'hud_hca_api_map_container', 'mapbox.streets' )
      .setView( [40, -80], 2 );

    if (hud_data.counseling_agencies) {
      update_map( hud_data );
    }
  }

  $( document ).ready( initialize_map );

  /*	generate_google_map(data) takes the data and plots the markers, etc, on
  the google map. It's called by get_counselors_by_zip(). */

  function update_map( data ) {
    // reset the map
    for (var i = 0; i < marker_array.length; i++ ) {
      map.removeLayer( marker_array[i] );
    }
    marker_array = [];
    if ( zip_marker != null ) {
      map.removeLayer( zip_marker );
    }
    map.setZoom( 2 );
    map.setView( [40, -80] );

    if ( cfpb_hud_hca.check_hud_data( data ) === true ) {
      var lat = data.zip.lat;
      var lng = data.zip.lng;
      var ziplatlng = [lat, lng];
      var zoom = 14;

      map.setZoom( zoom );
      map.setView( ziplatlng );

      var bounds = map.getBounds();
      var xmax = -Infinity;
      var xmin = Infinity;
      var ymax = -Infinity;
      var ymin = Infinity;

      zip_marker = L.circle( ziplatlng, 3 ).addTo( map );

      $.each( data.counseling_agencies, function( i, val ) {
        var lat = val.agc_ADDR_LATITUDE;
        var lng = val.agc_ADDR_LONGITUDE
        var position = new L.LatLng( lat, lng );

        if ( lat > ymax ) ymax = lat;
        if ( lat < ymin ) ymin = lat;
        if ( lng > xmax ) xmax = lng;
        if ( lng < xmin ) xmin = lng;

        var number = i + 1;

        if ( number < 10 ) {
          number = '0' + number;
        }

        var icon = L.icon({
          iconUrl: '/static/nemo/_/img/hud_gmap/agc_' + number + '.png',
          iconAnchor: [20, 50]
        } );

        var marker = new L.Marker( position, { icon: icon } ).addTo( map );
        marker_array[i] = marker;

        marker.on( 'click', function() {
          $( document.body ).animate( { 'scrollTop': $( '#hud-result-' + number ).offset().top }, 1000);
        } );
      } );

      //shift the max bounds so that the dropped pins are always on screen
      var xd = ( xmax - xmin ) / 10;
      var yd = ( ymax - ymin ) / 10;

      map.fitBounds( [[ymin - yd, xmin - xd], [ymax + yd, xmax + xd]] );
    }
  }

  $( document ).ready( function() {

    // On click of the print link, open print dialog
    $( '.hud_hca_api_no_js_print_text' ).remove();
    $( '.hud_hca_api_results_print' ).append( '<a class="hud-hca-api-print" href="#print">Print list</a>' );
    $( '.hud_hca_api_results_print a.hud-hca-api-print' ).click( function() {
      window.print();
      return false;
    } );

    // Provide a fallback for HTML5 placeholder for older browsers
    $( '#hud_hca_api_query', function() {
      var input = document.createElement( 'input' );
      if ( ( 'placeholder' in input ) == false ) {
        $( '[placeholder]' ).focus( function() {
          var i = $( this );
          if ( i.val() == i.attr( 'placeholder' ) ) {
            i.val( '' ).removeClass( 'placeholder' );
          }
        } ).blur(function() {
          var i = $( this );
          if ( i.val() == '' || i.val() == i.attr( 'placeholder' ) ) {
            i.addClass( 'placeholder' ).val(i.attr( 'placeholder' ) );
          }
        } ).blur().parents( 'form' ).submit( function() {
          $( this ).find( '[placeholder]' ).each(function() {
            var i = $( this );
            if ( i.val() == i.attr( 'placeholder' ) )
            i.val( '' );
          } )
        } );
      }
    } );

    // If there is a GET value for zip, load that zip immediately.
    var getzip = get_url_zip();
    if ( getzip != '' ) {
      $( '#hud_hca_api_query' ).val( getzip );
      $( '.hud_hca_api_form_button' ).trigger( 'click' );
    }

  } );

} )( jQuery, L ); // end anonymous function capsule
