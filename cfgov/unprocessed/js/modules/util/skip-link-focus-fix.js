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
  focusOnElement( skipNavEl );

  // if the hash has been changed (activation of an in-page link)
  // @todo this will only work if the "back-to-top" link has a value instead of # :(
  // i can call focusEl manually on that link..
  window.addEventListener('hashchange', function() {
    console.log('The hash has changed!');
    let hash = '#' + window.location.hash.replace( /^#/, '' );
    let focusEl = document.querySelector( hash );
    focusOnElement( focusEl );
    // console.log ( focusEl );

  }, false);
   
    // $(document).ready(function(){
    //   // if there is a '#' in the URL (someone linking directly to a page with an anchor)
    //   if (document.location.hash) {
    //     focusOnElement($(document.location.hash));
    //   }

    // jQuery.extend(jQuery.expr[':'], {
    //   focusable: function(el, index, selector){
    //     var $element = $(el);
    //     return $element.is(':input:enabled, a[href], area[href], object, [tabindex]') && !$element.is(':hidden');
    //   }
    // });

}

function focusOnElement( $element ) {
  if ( !$element ) {
    console.log ( 'no' );
    console.log ( $element );
    return;
  }

  console.log ( $element );
  // if ( !$element.is( ':focusable' ) ) {
    // add tabindex to make focusable and remove again
  $element.setAttribute( 'tabindex', '-1' );
  $element.style.background = 'aqua';

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
