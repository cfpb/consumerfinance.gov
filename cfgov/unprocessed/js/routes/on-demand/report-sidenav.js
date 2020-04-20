/* ==========================================================================
   Scripts for Report Sidenav organism
   ========================================================================== */

const sidenav = document.querySelector( '.o-report-sidenav' );
const top = sidenav.offsetTop;
let set = 0;

function stickOnScroll( e ) {
  if ( window.scrollY > top ) {
    if ( !set ) {
      sidenav.classList.add( 'sticky' );
      set = 1;
    }
  } else if ( set ) {
    sidenav.classList.remove( 'sticky' );
    set = 0;
  }
}

window.addEventListener( 'scroll', stickOnScroll );
stickOnScroll();
