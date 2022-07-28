/* eslint-disable complexity, no-undefined */
/* ==========================================================================
   Scripts for Report Sidenav organism
   ========================================================================== */

const main = document.querySelector( 'main' );
const sidenav = main.querySelector( '.o-report-sidenav' );
const tocHeaders = sidenav.querySelectorAll( '.m-nav-link' );
const headerOffset = main.offsetTop - 10;
const headers = main.querySelectorAll( 'h2.report-header, h3.report-header' );

const offsets = [];
const primaryOffsets = [];
let lastTargetIndex;

// Initialize offsets for calculating what to highlight
( function() {
  for ( let i = 0; i < headers.length; i++ ) {
    offsets.push( headers[i].offsetTop + headerOffset );
    primaryOffsets.push( headers[i].tagName === 'H2' );
  }
} )();

// Keep sidenav content from clipping into footer
document.querySelector( '.o-footer' ).classList.add( 'report-global-footer' );

// Set sidebar height on parent of sticky sidenav
sidenav.parentElement.style.height = main.clientHeight + 'px';

/**
 * Gets the node in the sidenav that wraps the section and subsections
 * @param {number} index from which to search for the parent
 * @returns {object} The parent node of the section
 **/
function getParentHeader( index ) {
  for ( let i = index; i >= 0; i-- ) {
    if ( primaryOffsets[i] ) return tocHeaders[i].parentNode;
  }
  return null;
}

/**
 * Highlights the appropriate sidenav header and reveals children on scroll
 **/
function hightlightTOC() {
  const sY = window.scrollY;
  const len = offsets.length;

  for ( let i = 0; i <= len; i++ ) {
    if ( i === len || sY < offsets[i] ) {
      const hl = i ? i - 1 : i;
      if ( hl === lastTargetIndex ) return;

      if ( lastTargetIndex !== undefined ) {
        tocHeaders[lastTargetIndex].classList.remove( 'm-nav-link__current' );
        getParentHeader( lastTargetIndex ).classList.remove( 'parent-header' );
      }

      tocHeaders[hl].classList.add( 'm-nav-link__current' );
      getParentHeader( hl ).classList.add( 'parent-header' );
      lastTargetIndex = hl;
      return;
    }
  }
}

window.addEventListener( 'scroll', hightlightTOC );
hightlightTOC();
