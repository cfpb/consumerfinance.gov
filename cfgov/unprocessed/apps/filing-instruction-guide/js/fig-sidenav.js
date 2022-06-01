/* eslint-disable */
/* ==========================================================================
   Scripts for Report Sidenav organism
   ========================================================================== */

import { buildMobileTOC } from "./fig-toc-frame";
const sidenav = document.querySelector( '.o-report-sidenav' );
const tocHeaders = document.querySelectorAll( '.o-report-sidenav .m-nav-link' );
const top = sidenav.offsetTop;
const headerOffset = 224
const headers = document.querySelectorAll( '.content_main .report-header' )
let offsets = [];
let primaryOffsets = [];
let set = 0;
let lastTargetIndex;

(function(){
  for(let i=0; i<headers.length; i++){
    offsets.push(headers[i].offsetTop + headerOffset)
    primaryOffsets.push(headers[i].tagName === 'H2')
  }
})();

document.querySelector('.o-footer').classList.add( 'report-global-footer' );

let mobileTOC = buildMobileTOC();

function scrunchIfNeeded() {
  let screenX = window.innerWidth || document.documentElement.clientWidth || document.getElementsByTagName('body')[0].clientWidth;
  if (screenX < 900) {
      sidenav.classList.add( 'scrunch' );
      sidenav.appendChild(mobileTOC);
      let tocContent = document.querySelector( '.toc-expandable_content' );
      for (let i = 0; i < sidenav.children.length; i++){
        if (sidenav.children[i].className !== 'toc-div'){
          if (sidenav.children[i].tagName !== 'H3'){
            tocContent.appendChild(sidenav.children[i]);
          } else {
            sidenav.children[i].style.display = 'none';
          }
        }
      }
      
  } else {
      sidenav.classList.remove( 'scrunch' );
      let tocContent = document.querySelector( '.toc-expandable_content' );
      for (let i = 0; i < tocContent.children.length; i ++){
        sidenav.append(tocContent.children[i]);
      }
      sidenav.removeChild(document.querySelector('.toc-div'));
      for (let i = 0; i < sidenav.children.length; i++){
        sidenav.children[i].style.display = 'block';
      }
  }
}

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

window.addEventListener( 'scroll', onScroll );
window.addEventListener( 'resize', scrunchIfNeeded );

onScroll();
scrunchIfNeeded();
