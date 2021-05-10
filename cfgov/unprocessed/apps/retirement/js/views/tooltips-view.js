// TODO: remove jquery.
import $ from 'jquery';

let currentTooltip;

function init() {
  // Tooltip handler
  const tooltipHandlers = document.querySelectorAll( '[data-tooltip-target]' );
  let tooltip;
  for ( let i = 0, len = tooltipHandlers.length; i < len; i++ ) {
    tooltip = tooltipHandlers[i];
    tooltip.addEventListener( 'click', function( ev ) {
      ev.preventDefault();
      ev.stopPropagation();
      toolTipper( ev.currentTarget );
    } );
  }
}

function toolTipper( elem ) {
  // position tooltip-container based on the element clicked.
  const $elem = $( elem );
  const $ttc = $( '#tooltip-container' );
  const name = elem.getAttribute( 'data-tooltip-target' );
  const contentSel = `[data-tooltip-name="${ name }"]`;
  const content = document.querySelector( contentSel ).innerHTML;
  const innerTip = $ttc.find( '.innertip' );
  const outerTip = $ttc.find( '.outertip' );
  const pageSel = '#main .content_wrapper';
  let pagePadding = parseInt( $( pageSel ).css( 'padding-left' ), 10 );
  let newLeft;
  let elemCenter;
  let elemRightOffset;

  $ttc.width( $( '#claiming-social-security' ).width() / 3 );

  $ttc.find( '.content' ).html( content );
  currentTooltip = $elem;

  $ttc.show();
  const newTop = $elem.offset().top + $elem.outerHeight() + 10;
  newLeft = $elem.offset().left + $elem.outerWidth() / 2 -
            $ttc.outerWidth( true ) / 2;
  $ttc.css( { top: newTop, left: newLeft } );

  // check offset again, properly set tips to point to the element clicked
  const tipOffset = Math.floor( $ttc.outerWidth() / 2 );
  innerTip.css( 'left', Math.floor( tipOffset - innerTip.outerWidth() / 2 ) );
  outerTip.css( 'left', Math.floor( tipOffset - outerTip.outerWidth() / 2 ) );

  // Prevent tooltip from falling off the left side of screens
  if ( newLeft < pagePadding ) {
    elemCenter = $elem.offset().left + $elem.width() / 2;
    $ttc.css( 'left', pagePadding );
    innerTip.css(
      'left',
      elemCenter - innerTip.outerWidth() / 2 - pagePadding
    );
    outerTip.css(
      'left',
      elemCenter - outerTip.outerWidth() / 2 - pagePadding
    );
  }

  // Prevent tooltip from falling off the right side of screens
  if ( $ttc.offset().left + $ttc.outerWidth( true ) > $( window ).width() ) {
    elemCenter = $elem.offset().left + $elem.width() / 2;
    elemRightOffset = $( window ).width() - elemCenter;
    newLeft = $( window ).width() - $ttc.outerWidth( true ) - pagePadding;
    $ttc.css( 'left', newLeft );
    innerTip.css(
      'left',
      $ttc.outerWidth() - innerTip.outerWidth() / 2 -
      elemRightOffset + pagePadding
    );
    outerTip.css(
      'left',
      $ttc.outerWidth() - outerTip.outerWidth() / 2 -
      elemRightOffset + pagePadding
    );
  }

  // if userAgent is an iPhone, iPad, iPod
  if ( ( /iP/i ).test( navigator.userAgent ) ) {
    // make the body clickable
    $( 'body' ).css( 'cursor', 'pointer' );
  }

  document.body.addEventListener( 'click', function() {
    document.onclick = function() {
      // iPhone Safari fix?
    };
    $ttc.hide();
    $ttc.find( '.content' ).html( '' );
    currentTooltip = null;
  } );

  window.addEventListener( 'resize', function() {
    if ( $( '#tooltip-container' ).is( ':visible' ) ) {
      $( '#tooltip-container' ).hide();
      toolTipper( $( '[data-tooltip-current-target]' ) );
    }
  } );
}

export default {
  init
};
