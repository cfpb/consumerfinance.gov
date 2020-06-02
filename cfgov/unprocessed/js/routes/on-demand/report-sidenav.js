/* eslint-disable */
/* ==========================================================================
   Scripts for Report Sidenav organism
   ========================================================================== */

const sidenav = document.querySelector( '.o-report-sidenav' );
const tocHeaders = document.querySelectorAll( '.o-report-sidenav .m-nav-link' );
const top = sidenav.offsetTop;
const headerOffset = 224
const headers = document.querySelectorAll( '.content_main .report-header' )
let offsets = [];
let offsetIsH3 = [];
let set = 0;
let lastTargetIndex;

(function(){
  for(let i=0; i<headers.length; i++){
    offsets.push(headers[i].offsetTop + headerOffset)
    offsetIsH3.push(headers[i].tagName === 'H3')
  }
})();

document.querySelector('.o-footer').classList.add( 'report-global-footer' );


function stickIfNeeded() {
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
    if(offsetIsH3[i]) return tocHeaders[i].parentNode
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
        tocHeaders[lastTargetIndex].classList.remove( 'current-section' );
        getParentHeader(lastTargetIndex).classList.remove('parent-header')
      }

      tocHeaders[hl].classList.add( 'current-section' );
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

window.addEventListener( 'scroll', onScroll );
onScroll();
