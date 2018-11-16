const jQuery = require( 'jquery' );

let UNDEFINED;

/* This script uses a local Django API to acquire a list of the 10 closest
HUD Counselors by zip code. See hud_api_replace for more details on the
API queries. -wernerc */

/* This class represents a namespace of functions that should be exposed
for testing purposes. */
const cfpb_hud_hca = ( function() {
  /* check_zip() is an easy, useful function that takes a string and returns a valid zip code, or returns false.
  NOTE: 'Valid' means 5 numeric characters, not necessarily 'existant' and 'actually addressable.' */
  const check_zip = function( zip ) {
    if ( ( zip === null ) || ( zip === UNDEFINED ) || ( zip === false ) ) {
      return false;
    }

    zip = zip.toString().replace( /[^0-9]+/g, '' );
    zip = zip.slice( 0, 5 );
    if ( zip.length === 5 ) {
      return zip;
    }

    return false;


  };

  /* check_data_structure() just makes sure your data has the correct structure before you start
  requesting properties that don't exist in generate_html() and update_map() */
  const check_hud_data = function( data ) {
    if ( ( data === null ) || ( data === 0 ) || ( data === UNDEFINED ) ) {
      return false;
    } else if ( data.hasOwnProperty( 'error' ) ) {
      return 'error';
    } else if ( !data.hasOwnProperty( 'counseling_agencies' ) ) {
      return false;
    } else if ( !data.hasOwnProperty( 'zip' ) ) {
      return false;
    }

    return true;

  };

  return {
    check_zip: check_zip,
    check_hud_data: check_hud_data
  };
} )();

( function( $, L ) { // start jQuery capsule

  let map;
  let marker_array = [];
  let zip_marker = null;


  /* get_url_zip() is a simple function to retrieve the zip variable from the URL */
  function get_url_zip() {
    let zip = '';
    const keyvals = window.location.href.slice( window.location.href.indexOf( '?' ) + 1 ).split( '&' );
    $.each( keyvals, function( i, val ) {
      const parts = val.split( '=' );
      if ( parts[0] === 'zip' ) {
        zip = parts[1];
      }
    } );
    return cfpb_hud_hca.check_zip( zip );
  }

  /* initialize_map() sets options and creates the map */
  function initialize_map() {
    L.mapbox.accessToken = window.mapbox_access_token;
    map = L.mapbox.map( 'hud_hca_api_map_container', 'mapbox.streets' )
      .setView( [ 40, -80 ], 2 );

    if ( window.hud_data.counseling_agencies ) {
      update_map( window.hud_data );
    }
  }

  $( document ).ready( initialize_map );

  /* generate_google_map(data) takes the data and plots the markers, etc, on
  the google map. It's called by get_counselors_by_zip(). */

  function update_map( data ) {
    // reset the map
    for ( let i = 0; i < marker_array.length; i++ ) {
      map.removeLayer( marker_array[i] );
    }
    marker_array = [];
    if ( zip_marker !== null ) {
      map.removeLayer( zip_marker );
    }
    map.setZoom( 2 );
    map.setView( [ 40, -80 ] );

    if ( cfpb_hud_hca.check_hud_data( data ) === true ) {
      const lat = data.zip.lat;
      const lng = data.zip.lng;
      const ziplatlng = [ lat, lng ];
      const zoom = 14;

      map.setZoom( zoom );
      map.setView( ziplatlng );

      const bounds = map.getBounds();
      let xmax = -Infinity;
      let xmin = Infinity;
      let ymax = -Infinity;
      let ymin = Infinity;

      zip_marker = L.circle( ziplatlng, 3 ).addTo( map );

      $.each( data.counseling_agencies, function( i, val ) {
        const lat = val.agc_ADDR_LATITUDE;
        const lng = val.agc_ADDR_LONGITUDE;
        const position = new L.LatLng( lat, lng );

        if ( lat > ymax ) ymax = lat;
        if ( lat < ymin ) ymin = lat;
        if ( lng > xmax ) xmax = lng;
        if ( lng < xmin ) xmin = lng;

        let number = i + 1;

        if ( number < 10 ) {
          number = '0' + number;
        }

        const icon = L.icon( {
          iconUrl: '/static/nemo/_/img/hud_gmap/agc_' + number + '.png',
          iconAnchor: [ 20, 50 ]
        } );

        const marker = new L.Marker( position, { icon: icon } ).addTo( map );
        marker_array[i] = marker;

        marker.on( 'click', function() {
          $( document.body ).animate( { scrollTop: $( '#hud-result-' + number ).offset().top }, 1000 );
        } );
      } );

      // shift the max bounds so that the dropped pins are always on screen
      const xd = ( xmax - xmin ) / 10;
      const yd = ( ymax - ymin ) / 10;

      map.fitBounds( [ [ ymin - yd, xmin - xd ], [ ymax + yd, xmax + xd ] ] );
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
      const input = document.createElement( 'input' );
      if ( ( 'placeholder' in input ) === false ) {
        // eslint-disable-next-line max-nested-callbacks
        $( '[placeholder]' ).focus( function() {
          const i = $( this );
          if ( i.val() === i.attr( 'placeholder' ) ) {
            i.val( '' ).removeClass( 'placeholder' );
          }
        // eslint-disable-next-line max-nested-callbacks
        } ).blur( function() {
          const i = $( this );
          if ( i.val() === '' || i.val() === i.attr( 'placeholder' ) ) {
            i.addClass( 'placeholder' ).val( i.attr( 'placeholder' ) );
          }
        // eslint-disable-next-line max-nested-callbacks
        } ).blur().parents( 'form' ).submit( function() {
          // eslint-disable-next-line max-nested-callbacks
          $( this ).find( '[placeholder]' ).each( function() {
            const i = $( this );
            if ( i.val() === i.attr( 'placeholder' ) ) i.val( '' );
          } );
        } );
      }
    } );

    // If there is a GET value for zip, load that zip immediately.
    const getzip = get_url_zip();
    if ( getzip !== '' ) {
      $( '#hud_hca_api_query' ).val( getzip );
      $( '.hud_hca_api_form_button' ).trigger( 'click' );
    }

  } );

} )( jQuery, window.L ); // end anonymous function capsule
