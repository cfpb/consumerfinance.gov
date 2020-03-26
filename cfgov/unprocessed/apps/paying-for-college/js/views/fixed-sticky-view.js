import { bindEvent } from '../../../../js/modules/util/dom-events';

const fixedSticky = {
  _stickies: null,
  _sticky: null,
  _offset: 0,
  _stickyHeight: 0,
  _scrollTimeout: null,
  _appSegment: null,

  /**
     * scrollY - Get the Y coord of the current viewport. Older browsers don't
     * support `scrollY` so use whichever works.
     *
     * @returns {function} Browser-supported y offset method.
     */
  scrollY: () => window.scrollY || window.pageYOffset,

  /**
     * getYLocation - Get Y location of provided element on the page.
     *
     * @param {node} el HTML element
     *
     * @returns {type} Description
     */
  getYLocation: el => {
    const elOffset = el.getBoundingClientRect().top;
    return fixedSticky.scrollY();
  },

  _scrollHandler: function( event ) {
    fixedSticky._stickies.forEach( elem => {
      const yLoc = fixedSticky.getYLocation( elem );
      const scrollY = fixedSticky.scrollY();
      const limit = fixedSticky._collegeCosts.offsetTop + fixedSticky._collegeCosts.offsetHeight -
        ( window.innerHeight / 2 );

      if ( scrollY > fixedSticky._offset && scrollY <= limit ) {
        // elem.style.top = scrollY - fixedSticky._offset + 'px';
        const right = ( window.innerWidth - fixedSticky._appSegment.offsetWidth ) / 2;
        elem.classList.add( 'stuck' );
        elem.style.right = right + 'px';
      } else {
        elem.classList.remove( 'stuck' );
        elem.style.right = '0px';
      }
    } );

  },

  _scrollListener: function() {
    const events = {
      scroll: this._scrollHandler
    };
    bindEvent( window, events );
  },

  init: function( selector ) {
    this._stickies = document.querySelectorAll( selector );
    // this._sticky = elem;
    this._collegeCosts = document.querySelector( '.college-costs' );
    this._appSegment = document.querySelector( '.college-costs_app-segment' );
    this._offset = this._collegeCosts.offsetTop;
    this._scrollListener();
  }
};

export {
  fixedSticky
};
