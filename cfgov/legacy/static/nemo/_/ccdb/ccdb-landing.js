'use strict';

var urlCodes = {
  'all_all' : 's6ew-h6mp',
  'all_narratives' : 'nsyy-je5y',
  'bank-account_all' : 't9fg-cqmi',
  'bank-account_narratives' : 'ytxv-uppu',
  'credit-card_all' : '7zpz-7ury',
  'credit-card_narratives' : 'wycs-qcs4',
  'credit-reporting_all' : 'xa48-juie',
  'credit-reporting_narratives' : 'ur78-i5sn',
  'debt-collection_all' : 'ckyu-ku28',
  'debt-collection_narratives' : 'dx9u-5nhx',
  'money-transfer_all' : 'uha4-cwwn',
  'money-transfer_narratives' : 'njq8-tnnk',
  'mortgage_all' : 'g5qz-smft',
  'mortgage_narratives' : 'gfmg-6ppu',
  'other_all' : 'b239-tvpx',
  'other_narratives' : 'yjne-fppi',
  'payday-loan_all' : '6hp8-hzag',
  'payday-loan_narratives' : 'xiq2-ahjv',
  'prepaid-card_all' : '6yuf-367p',
  'prepaid-card_narratives' : '2t2q-2pud',
  'student-loan_all' : 'eew7-9yf2',
  'student-loan_narratives' : 'j875-kipn',
  'consumer-loan_all' : 'wfbn-zkat',
  'consumer-loan_narratives' : 'uqjt-9neg'
};

var lastClicked = 'bank-account'; // Tracks the last thing the user clicked to respond to window resize

/**
  * Reformats "2015-01-31" style date to "1/31/2015" style
  * @param { string } date - A date of a 2015-01-31 format
  * @returns { string } A date of the 1/31/2015 format
  */
function dateReformat( date ) {
  if ( typeof date === 'undefined' ) {
    return '';
  }
  var reformatted = date.substr( 0, 10 ),
      arr = reformatted.split('-');
  reformatted = Number(arr[1]).toString() + '/' + Number(arr[2]).toString() + '/' + Number(arr[0]).toString();
  return reformatted;
}

/**
  * Inserts text into selector after performing some cleanup activities and checks against
  * undefined values.
  * @param { string } selector - A selector, a la CSS/jQuery
  * @param { string } text - The text to be placed in the element
  * @param { string } flag - Flags that help with the formatting
  */
jQuery.fn.extend({
  insertText: function ( selector, text, flag ) {
    if ( typeof text === 'undefined' ) {
      text = ' ';
    }
    if ( text === null ) {
      text = 'None';
    }
    if ( flag === 'quoted' ) {
      text = '"' + text.trim() + '"';
    }
    if ( flag === 'number' ) {
      text = numToString( text );
    }
    if ( flag === 'percent' ) {
      text += '%';
    }
    if ( flag === 'date' ) {
      text = dateReformat( text );
    }

    $(this).find( selector ).text( text );
  }
});


/**
  * Assigns handlers to tooltips
  * @param { object } $elem - jQuery object
  */
function toolTipper( $elem ) {
  // position tooltip-container based on the element clicked
  var ttc = $('#tooltip-container'),
      name = $elem.attr('data-tooltip-target'),
      content = $('[data-tooltip-name="' + name + '"]').html(),
      innerTip = ttc.find( '.innertip' ),
      outerTip = ttc.find( '.outertip' ),
      newTop,
      newLeft,
      tipset,
      tipOffset;

  ttc.width( $('#ccdb-landing').width() / 3 );

  ttc.find('.content').html( content );
  $('[data-tooltip-current-target]').removeAttr('data-tooltip-current-target');
  $elem.attr( 'data-tooltip-current-target', true );

  ttc.show();
  newTop = $elem.offset().top + $elem.outerHeight() + 10;
  newLeft = $elem.offset().left + ( $elem.outerWidth() / 2 ) - ( ttc.outerWidth(true) / 2 );
  ttc.css( { 'top': newTop, 'left': newLeft } );

  if ( ttc.offset().left + ttc.outerWidth(true) > $(window).width()) {
    newLeft = $(window).width() - ttc.outerWidth(true) - 20;
    ttc.css( 'left', newLeft );
  }
  // check offset again, properly set tips to point to the element clicked
  tipOffset = Math.floor( ttc.outerWidth() / 2 );
  innerTip.css('left', Math.floor( tipOffset - ( innerTip.outerWidth() / 2 ) ) );
  outerTip.css('left', Math.floor( tipOffset - ( outerTip.outerWidth() / 2 ) ) );

  $( 'html' ).on('click', 'body:not(#tooltip-container a)', function() {
    ttc.hide();
    ttc.find( '.content' ).html('');
    $('[data-tooltip-current-target]').removeAttr('data-tooltip-current-target');
    $( 'html' ).off('click');
  });
}

/**
  * Convert from number to number string (with commas)
  * @param { number } n - A number
  * @returns { string } - A string that looks like a number with commas!
  */
function numToString(n) {
  return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

$(document).ready( function() {
  var dataURL = 'http://files.consumerfinance.gov/ccdb/narratives.json',
      countURL = 'https://data.consumerfinance.gov/resource/u473-64qt.json',
      response = '',
      remaps = { 'bank-account' : 'bank_accounts',
                'credit-card' : 'credit_cards',
                'credit-reporting' : 'credit_reporting',
                'debt-collection' : 'debt_collection',
                'money-transfer' : 'money_transfers',
                'mortgage' : 'mortgages',
                'other' : 'other_financial_services',
                'payday-loan' : 'payday_loans',
                'prepaid-card' : 'prepaid_cards',
                'student-loan' : 'student_loans',
                'consumer-loan' : 'other_consumer_loans'
                };

  $.ajax({
    url: dataURL,
    dataType: 'JSONP',
    jsonp: false,
    jsonpCallback: 'narratives',
    success: function( data ) {
      $( '.complaint-container' ).each( function() {
        var category = $(this).attr( 'data-container-for' ),
            complaintData = data[ remaps[ category ] ];

        if ( remaps.hasOwnProperty( category ) !== -1 ) { // Don't look for complaint data in data.stats!
          // Set complaint data text
          $(this).insertText( '.complaint-text', complaintData.complaint_what_happened );
          $(this).insertText( '.response-text', complaintData.company_public_response );
          $(this).insertText( '.complaint-company-response', complaintData.company_response );
          $(this).insertText( '.complaint-subproduct', complaintData.sub_product );
          $(this).insertText( '.complaint-issue', complaintData.issue );
          $(this).insertText( '.complaint-state', complaintData.state );
          $(this).insertText( '.complaint-date', complaintData.date_received, 'date' );
        }

      });
      if ( data.hasOwnProperty( 'stats' ) ) {
        $( '#ccdb-landing' ).insertText( '.percent-timely', data.stats.percent_timely, 'percent' );
      }
    }
  });

  $.get( countURL )
    .done( function( data ) {
      var complaintCount = 0,
          responseCount = 0;
      $.each( data, function( i, val ) {
        complaintCount += Number( val.count_complaint_id );
        if ( val.company_response !== 'Untimely response' ) {
          responseCount += Number( val.count_complaint_id );
        }
      });
      $( '#ccdb-landing' ).insertText( '.total-complaints', complaintCount, 'number' );
      $( '#ccdb-landing' ).insertText( '.company-responses', responseCount, 'number' );

    });

  $( '.category-buttons button' ).click( function() {
    lastClicked = $(this).attr('data-category');
    $('.category-buttons button').removeClass('selected-button');
    $(this).addClass('selected-button');
    $('.complaint-container').hide();
    $( '.complaint-container[data-container-for="' + lastClicked + '"]' ).show();
  });

  $( '.category-buttons button' ).hover(
    function() {
      var $textBox = $(this).find('.text-content');
      $(this).addClass('hover-button');
      $textBox.css( 'left', ( $textBox.outerWidth() - $(this).outerWidth() ) / 2 * -1 );
    },
    function() {
      $(this).removeClass('hover-button');
    }
  );

  $( 'button.category-next' ).click( function() {
    lastClicked = $(this).attr('data-category');
    $('.category-buttons button[data-category="' + lastClicked + '"]').click();
  });

  $( '.expandable-bar' ).click( function() {
    var $complaint = $( '.complaint-container[data-container-for="' + $(this).attr('data-category') + '"]' );
    if ( $complaint.is(':visible') ) {
      $complaint.slideUp();
      $(this).find('.cf-icon-minus-round').removeClass('cf-icon-minus-round').addClass('cf-icon-plus-round');
    } else {
      $complaint.slideDown();
      $(this).find('.cf-icon-plus-round').removeClass('cf-icon-plus-round').addClass('cf-icon-minus-round');
      lastClicked = $(this).attr( 'data-category' );
    }
  });

  // Show the Bank accounts tab on load.
  if ( $('.category-buttons').is(':visible') ) {
    $( '.category-buttons button' )[0].click();
  }

  // Responsive header fix
  var html = '<a class="toggle-menu" href="#"><span class="cf-icon cf-icon-menu"></span><span class="u-visually-hidden">Menu</span></a>';
  $( '#header > div:first-child' ).prepend( html );
  var bodyTag = document.getElementsByTagName('body')[0];
  bodyTag.className += ' js';
  $( '.toggle-menu' ).on( 'click', function() {
    $( '#header > nav ul' ).toggleClass( 'vis' );
  });

  // Tooltip handler
  $('[data-tooltip-target]').click( function( ev ) {
    ev.preventDefault();
    ev.stopPropagation();
    toolTipper( $(this) );
  });

  // Tooltip resize handler
  $(window).resize( function() {
    if ( $('#tooltip-container').is(':visible') ) {
      $('#tooltip-container').hide();
      toolTipper( $('[data-tooltip-current-target]') );
    }
  });

  $('.download-radio').click( function() {
    var url = 'https://data.consumerfinance.gov/views/',
        category = $('.download-radio input:checked').val(),
        include = $('#download_include option:selected').val(),
        code = urlCodes[category + '_' + include],
        format = $('#download_format option:selected').val();
    $('#download-data-btn').attr( 'href', url + code + '/rows.' + format );
  });

  $('#download_format, #download_include').on( 'change', function() {
    $('.download-radio input:checked').click();
  });

  $('.publication-criteria a, .list__links .pdf, .pdf').removeClass('pdf');

  $( window ).resize( function() {
    if ( $( '.category-buttons' ).is( ':visible' ) ) {
      $( '.category-buttons button[data-category="' + lastClicked + '"]' ).click();
    } else {
      $( '.complaint-container:visible' ).each( function() {
        var $expandableBar = $( '.expandable-bar[data-category="' + lastClicked + '"]' );
        lastClicked = $( this ).attr( 'data-container-for' );
        $expandableBar.find( '.cf-icon-plus-round' ).removeClass( 'cf-icon-plus-round' ).addClass( 'cf-icon-minus-round' );
      });
    }
  });

});
