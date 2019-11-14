import { bindEvent } from '../../../../js/modules/util/dom-events';

const fixedSticky = {
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
    const yLoc = fixedSticky.getYLocation( fixedSticky._sticky );
    const scrollY = fixedSticky.scrollY();
    const limit = fixedSticky._collegeCosts.offsetTop + fixedSticky._collegeCosts.offsetHeight -
      ( window.innerHeight / 2 );


    console.log( scrollY, fixedSticky._offset, limit );

    if ( scrollY > fixedSticky._offset && scrollY <= limit ) {
      // fixedSticky._sticky.style.top = scrollY - fixedSticky._offset + 'px';
      const right = ( window.innerWidth - fixedSticky._appSegment.offsetWidth ) / 2;
      fixedSticky._sticky.classList.add( 'stuck' );
      fixedSticky._sticky.style.right = right + 'px';
    } else {
      fixedSticky._sticky.classList.remove( 'stuck' );
      fixedSticky._sticky.style.right = '0px';
    }
  },

  _scrollListener: function() {
    const events = {
      scroll: this._scrollHandler
    };
    bindEvent( window, events );
  },

  init: function( elem ) {
    this._sticky = elem;
    this._collegeCosts = document.querySelector( '.college-costs' );
    this._appSegment = document.querySelector( '.college-costs_app-segment' );
    this._offset = this._collegeCosts.offsetTop;
    this._scrollListener();
  }
};

export {
  fixedSticky
};
