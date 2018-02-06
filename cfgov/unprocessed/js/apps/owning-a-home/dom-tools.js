import fastDom from 'fastdom';

const NO_OP = function( ) {
  // Placeholder function meant to be overridden.
};

const DT = {
  applyAll: function( elements, applyFn ) {
    if ( elements instanceof HTMLElement ) {
      elements = [ elements ];
    }

    return [].slice.call( elements ).forEach( applyFn );
  },
  bindEvents: function( elements, events, callback = NO_OP ) {
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
  createElement: function( HTML ) {
    const div = document.createElement( 'div' );
    div.innerHTML = HTML;

    return div.firstChild;
  },
  removeClass: function( selector, className ) {
    className = className.split( ', ' );

    return DT.applyAll(
      DT.getEls( selector ),
      element => {
        fastDom.mutate( () =>
          element.classList.remove( ...className )
        );
      } );
  },
  addClass: function( selector, className ) {
    className = className.split( ', ' );

    return DT.applyAll(
      DT.getEls( selector ),
      element =>
        fastDom.mutate( () =>
          element.classList.add( ...className )
        )
    );
  },
  hasClass: function( selector, className ) {
    return DT.getEl( selector ).classList.contains( className );
  },
  getEls: function( selector ) {
    if ( DT.isEl( selector ) ) {
      return selector;
    }

    return document.querySelectorAll( selector );
  },
  getEl: function( selector ) {
    if ( DT.isEl( selector ) ) {
      return selector;
    }

    return document.querySelector( selector );
  },
  getPreviousEls: function( element, filter = '*' ) {
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
  isEl: function( element ) {
    return element instanceof NodeList ||
           element instanceof HTMLElement ||
           element instanceof Window;
  },
  hide: function( selector ) {
    return DT.applyAll( DT.getEls( selector ),
      element => fastDom.mutate(
        () => ( element.style.display = 'none' )
      )
    );
  },
  show: function( selector ) {
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
    window.setTimeout(
      () => {
        element.style.display = 'block';
        return callback();
      },
      time
    );
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
  nextFrame: function nextFrame( callback = NO_OP ) {
    const _nextFrame = window.requestAnimationFrame ||
                       window.webkitRequestAnimationFrame ||
                       window.mozRequestAnimationFrame ||
                       function( callback ) {
                         return setTimeout( function() {
                           callback( Number( new Date() ) );
                         }, 1000 / 60 );
                       };
    _nextFrame( callback );
  }
};

export default DT;

