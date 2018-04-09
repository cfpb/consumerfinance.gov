import fastDom from 'fastdom';

const NO_OP = function( ) {
  // Placeholder function meant to be overridden.
};

const DT = {
  applyAll: function applyAll( elements, applyFn ) {
    if ( elements instanceof HTMLElement ) {
      elements = [ elements ];
    }

    return [].slice.call( elements ).forEach( applyFn );
  },
  bindEvents: function bindEvents( elements, events, callback = NO_OP ) {
    if ( Array.isArray( events ) === false ) {
      events = [ events ];
    }

    if ( typeof elements === 'string' ) {
      elements = DT.getEls( elements );
    }

    DT.applyAll( elements, function( element ) {
      events.forEach( event => {
        element.addEventListener( event, callback );
      } );
    } );
  },
  createElement: function createElement( HTML ) {
    const div = document.createElement( 'div' );
    div.innerHTML = HTML;

    return div.firstChild;
  },
  removeClass: function removeClass( selector, className ) {
    className = className.split( ', ' );

    return DT.applyAll(
      DT.getEls( selector ),
      element => {
        fastDom.mutate( () =>
          element.classList.remove( ...className )
        );
      } );
  },
  addClass: function addClass( selector, className ) {
    className = className.split( ', ' );

    return DT.applyAll(
      DT.getEls( selector ),
      element =>
        fastDom.mutate( () =>
          element.classList.add( ...className )
        )
    );
  },
  hasClass: function hasClass( selector, className ) {
    return DT.getEl( selector ).classList.contains( className );
  },
  getEls: function getEls( selector ) {
    if ( DT.isEl( selector ) ) {
      return selector;
    }

    return document.querySelectorAll( selector );
  },
  getEl: function getEl( selector ) {
    if ( DT.isEl( selector ) ) {
      return selector;
    }

    return document.querySelector( selector );
  },
  getPreviousEls: function getPreviousEls( element, filter = '*' ) {
    const previousSiblings = [];
    let prevEl = element.previousElementSibling;
    function _getMatches( el ) {
      return el.matches ||
               el.webkitMatchesSelector ||
               el.mozMatchesSelector ||
               el.msMatchesSelector;
    }
    const _matchesMethod = _getMatches( element );

    while ( prevEl ) {
      if ( _matchesMethod.bind( prevEl )( filter ) ) {
        previousSiblings.push( prevEl );
      }
      prevEl = prevEl.previousElementSibling;
    }
    return previousSiblings;
  },
  isEl: function isEl( element ) {
    return element instanceof NodeList ||
           element instanceof HTMLElement ||
           element instanceof Window;
  },
  hide: function hide( selector ) {
    return DT.applyAll( DT.getEls( selector ),
      element => fastDom.mutate(
        () => ( element.style.display = 'none' )
      )
    );
  },
  show: function show( selector ) {
    return DT.applyAll( DT.getEls( selector ),
      element => fastDom.mutate(
        () => ( element.style.display = 'block' )
      )
    );
  },
  fadeIn: function fadeIn( element, time, callback = NO_OP ) {
    element.style.transition = 'opacity ' + time + 'ms ease-in-out';
    element.style.opacity = 0.05;
    element.style.display = 'block';
    window.setTimeout( () => ( element.style.opacity = 1 ), 100 );
    window.setTimeout( () => callback(), time );
  },
  fadeOut: function fadeOut( element, time, callback = NO_OP ) {
    element.style.transition = 'opacity ' + time + 'ms ease-in-out';
    element.style.opacity = 1;
    window.setTimeout( () => ( element.style.opacity = 0.05 ), 100 );
    window.setTimeout(
      () => {
        element.style.display = 'none';
        return callback();
      },
      time
    );
  },
  mutate: fastDom.mutate.bind( fastDom ),
  measure: fastDom.measure.bind( fastDom ),
  nextFrame: fastDom.raf
};

export default DT;

