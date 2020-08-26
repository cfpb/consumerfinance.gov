/* eslint-disable */
/* ==========================================================================
   Scripts for Report Sidenav organism
   ========================================================================== */

const sidenav = document.querySelector( '.o-report-sidenav' );
const tocHeaders = document.querySelectorAll( '.o-report-sidenav .m-nav-link' );
const top = sidenav.offsetTop;
const headerOffset = 224
const headers = document.querySelectorAll( '.content_main h2.report-header, .content_main h3.report-header' )
let isMobile
let offsets = [];
let primaryOffsets = [];
let set = 0;
let lastTargetIndex;

checkMatch();

(function(){
  for(let i=0; i<headers.length; i++){
    offsets.push(headers[i].offsetTop + headerOffset)
    primaryOffsets.push(headers[i].tagName === 'H2')
  }
})();

document.querySelector('.o-footer').classList.add( 'report-global-footer' );


function stickIfNeeded() {
  if(isMobile) return
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


function getParentHeader(index){
  for(let i=index; i>=0; i--){
    if(primaryOffsets[i]) return tocHeaders[i].parentNode
  }
}


function hightlightTOC() {
  const sY = window.scrollY;
  const len = offsets.length;

  for ( let i = 0; i <= len; i++ ) {
    if ( i === len || sY < offsets[i] ) {
      let hl = i ? i - 1 : i;
      if ( hl === lastTargetIndex ) return;
      if ( lastTargetIndex !== undefined ){
        tocHeaders[lastTargetIndex].classList.remove( 'm-nav-link__current' );
        getParentHeader(lastTargetIndex).classList.remove('parent-header')
      }

      tocHeaders[hl].classList.add( 'm-nav-link__current' );
      getParentHeader(hl).classList.add( 'parent-header' );
      lastTargetIndex = hl;
      return;
    }
  }
}


function onScroll() {
  stickIfNeeded();
  hightlightTOC();
}

function checkMatch() {
  isMobile = window.matchMedia('(max-width: 900px)').matches
}

window.addEventListener( 'scroll', onScroll );
window.addEventListener('resize', checkMatch);
onScroll();
