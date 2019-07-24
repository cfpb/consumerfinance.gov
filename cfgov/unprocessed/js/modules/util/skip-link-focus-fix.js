/**
 * Hack for Mobile Safari iOS 11 bug that doesn't move focus to anchor area
 * when in-page anchor links are clicked https://axesslab.com/skip-links/
 * @param   {(HTMLNode|string)} expr HTMLNode or string to query for
 * @param   {Object}          con  The document location to query
 * @returns {HTMLNode}             The elem
 */

function skipLinkFocusFix( ) {
  const skipNavLink = document.querySelector( '.skip-nav .skip-nav_link' ).getAttribute( 'href');
  const skipNavEl = document.querySelector( skipNavLink );
  console.log ( skipNavEl );
    
    // $(document).ready(function(){
    //   // if there is a '#' in the URL (someone linking directly to a page with an anchor)
    //   if (document.location.hash) {
    //     focusOnElement($(document.location.hash));
    //   }

    //   // if the hash has been changed (activation of an in-page link)
    //   $(window).bind('hashchange', function() {
    //     var hash = "#"+window.location.hash.replace(/^#/,'');
    //     focusOnElement($(hash));
    //   });
    // });

    // jQuery.extend(jQuery.expr[':'], {
    //   focusable: function(el, index, selector){
    //     var $element = $(el);
    //     return $element.is(':input:enabled, a[href], area[href], object, [tabindex]') && !$element.is(':hidden');
    //   }
    // });

  focusOnElement( skipNavEl );
}

function focusOnElement( $element ) {
  if ( !$element.length ) {
    return;
  }

  console.log ( $element );
  // if ( !$element.is( ':focusable' ) ) {
    // add tabindex to make focusable and remove again
  $element.setAttribute( 'tabindex', '-1' );

  $element.addEventListener( 'focusout', event => {
    event.target.style.background = 'magenta';
    event.target.removeAttribute( 'tabindex' );
  } );

    // $element.attr( 'tabindex', -1 ).on('blur focusout', function () {
    //   $(this).removeAttr('tabindex');
    // });
  // }
  $element.focus();
}

export {
  skipLinkFocusFix
};
