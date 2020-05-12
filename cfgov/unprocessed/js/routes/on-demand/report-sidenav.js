/* ==========================================================================
   Scripts for Report Sidenav organism
   ========================================================================== */

const sidenav = document.querySelector( '.o-report-sidenav' );
const tocHeaders = document.querySelectorAll( '.o-report-sidenav .m-nav-link' );
const offsets = Array.prototype.map.call(
  document.querySelectorAll( '.content_main .report-header' ),
  function( v ) { return v.offsetTop; }
);
const top = sidenav.offsetTop;
let set = 0;
let lastTargetIndex;

function stickIfNeeded( e ) {
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

function highlightTOC() {
  const sY = window.scrollY;
  const len = offsets.length - 1;
  for ( let i = 0; i <= len; i++ ) {
    if ( sY < offsets[i] ) {
      let next = i - 1;
      if ( next === -1 ) next = 0;
      if ( next === lastTargetIndex ) return;
      if ( lastTargetIndex !== undefined )tocHeaders[lastTargetIndex].classList.remove( 'current-section' );
      tocHeaders[next].classList.add( 'current-section' );
      lastTargetIndex = next;
      return;
    }
  }
  if ( lastTargetIndex !== undefined )tocHeaders[lastTargetIndex].classList.remove( 'current-section' );
  tocHeaders[len].classList.add( 'current-section' );
  lastTargetIndex = len;
}

function onScroll() {
  stickIfNeeded();
  highlightTOC();
}

window.addEventListener( 'scroll', onScroll );
onScroll();
