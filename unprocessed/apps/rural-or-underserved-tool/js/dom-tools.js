import fastDom from 'fastdom';

const NO_OP = function NO_OP( ) {
  // Placeholder function meant to be overridden.
};

const _matches = ( function _getMatches( ) {
  const el = document.body;
  return (
    el.matches ||
    el.webkitMatchesSelector ||
    el.mozMatchesSelector ||
    el.msMatchesSelector
  );
} )( );

function _mutate( selector, callback ) {
  applyAll( selector, function( element ) {
    fastDom.mutate( callback.bind( null, element ) );
  } );
}

/* Code copied from jQuery with minimal modifications.
   XHTML parsers do not magically insert elements in the
   same way that tag soup parsers do. So we cannot shorten
   this by omitting <tbody> or other required elements. */
const firstTag = /<([a-z][^\/\0>\x20\t\r\n\f]+)/;
const wrapMap = {
  'col':     [ 2, '<table><colgroup>', '</colgroup></table>' ],
  'default': [ 0, '', '' ],
  'option':  [ 1, '<select multiple=\'multiple\'>', '</select>' ],
  'td':      [ 3, '<table><tbody><tr>', '</tr></tbody></table>' ],
  'thead':   [ 1, '<table>', '</table>' ],
  'tr':      [ 2, '<table><tbody>', '</tbody></table>' ]
};

function applyAll( elements, applyFn ) {
  if ( elements instanceof HTMLElement ) {
    elements = [ elements ];
  } else if ( typeof elements === 'string' ) {
    elements = getEls( elements );
  }

  return [].slice.call( elements || [] ).forEach( applyFn );
}

function bindEvents( elements, events, callback ) {
  if ( Array.isArray( events ) === false ) {
    events = [ events ];
  }

  applyAll( elements, function( element ) {
    events.forEach( function( event ) {
      element.addEventListener( event, callback || NO_OP );
    } );
  } );
}

function addEl( parent, child ) {
  return fastDom.mutate( function( ) {
    const el = createEl( child );
    return getEl( parent ).appendChild( el );
  } );
}

function getElData( selector, attributeName ) {
  return getEl( selector )
    .getAttribute( 'data-' + attributeName );
}

function changeElText( selector, text ) {
  return _mutate( selector, function( element ) {
    return ( element.textContent = text );
  } );
}

function changeElHTML( selector, HTML ) {
  return _mutate( selector, function( element ) {
    return ( element.innerHTML = HTML );
  } );
}

// Code copied from jQuery with minimal modifications.
function createEl( HTML ) {
  if ( isEl( HTML ) ) {
    return HTML;
  }
  let container = document.createElement( 'div' );
  const tag = ( firstTag.exec( HTML ) || [ '', '' ] )[1].toLowerCase();
  const elWrapper = wrapMap[tag] || wrapMap.default;
  const docFrag = document.createDocumentFragment();
  container.innerHTML = elWrapper[1] + HTML + elWrapper[2];
  let wrapperCount = elWrapper[0];
  while ( wrapperCount-- ) {
    container = container.firstChild;
  }

  [].slice.call( container.childNodes ).forEach( function( node ) {
    docFrag.appendChild( node );
  } );

  return docFrag;
}

function removeEl( selector ) {
  return _mutate( selector, function( element ) {
    return element.parentNode.removeChild( element );
  } );
}

function addClass( selector, className ) {
  const classNames = [].slice.call( arguments ).slice( 1 );
  return _mutate( selector, function( element ) {
    let _classList;
    return ( _classList = element.classList )
      .add.apply( _classList, classNames );
  } );
}

function hasClass( selector, className ) {
  let _hasClass = false;
  applyAll( selector, function( element ) {
    if ( element.classList.contains( className ) ) {
      _hasClass = true;
    }
  } );
  return _hasClass;
}

function removeClass( selector, className ) {
  const classNames = [].slice.call( arguments ).slice( 1 );
  return _mutate( selector, function( element ) {
    let _classList;
    return ( _classList = element.classList )
      .remove.apply( _classList, classNames );
  } );
}

function toggleClass( selector, className ) {
  return _mutate( selector, function( element ) {
    return element.classList.toggle( className );
  } );
}

function filter( element, propName, filter ) {
  const _propName = propName || '';
  const _filter = filter || '*';

  const nodes = [];
  let node = element[propName];

  while ( node && node !== document ) {
    if ( _matches.call( node, _filter ) ) {
      nodes.push( node );
    }
    node = node[propName];
  }
  return nodes;
}

function getEl( selector ) {
  if ( isEl( selector ) ) {
    return selector;
  }
  return document.querySelector( selector );
}

function getEls( selector ) {
  if ( isEl( selector ) ) {
    return selector;
  }
  return document.querySelectorAll( selector );
}

function getChildEls( element, filter ) {
  const firstChild = element.childNodes[0];
  const elements = getNextEls( firstChild, filter );
  if ( firstChild.matches( filter ) ) {
    elements.unshift( firstChild );
  }
  return elements;
}

function getParentEls( element, filterNode ) {
  return filter( element, 'parentNode', filterNode );
}

function getPreviousEls( element, filterNode ) {
  return filter( element, 'previousElementSibling', filterNode );
}

function getNextEls( element, filterNode ) {
  return filter( element, 'nextElementSibling', filterNode );
}

function isEl( element ) {
  return (
    element instanceof NodeList ||
    element instanceof HTMLElement ||
    element instanceof DocumentFragment ||
    element instanceof Window
  );
}

/**
 * Check whether something is a NodeList, HTML element, or window.
 * @param {*} selector Something, possibly a list, element or window instance.
 * @returns {Function} Mutate dom function.
 */
function hide( selector ) {
  return _mutate( selector, function( element ) {
    return ( element.style.display = 'block' );
  } );
}

/**
 * Check whether something is a NodeList, HTML element, or window.
 * @param {*} selector Something, possibly a list, element or window instance.
 * @returns {Function} Mutate dom function.
 */
function show( selector ) {
  return _mutate( selector, function( element ) {
    return ( element.style.display = 'block' );
  } );
}

/**
 * @param {string} selector - Selector for an element.
 * @param {number} time - When to call the callback.
 * @param {[Function]} callback - Function to call after delay.
 */
function fadeIn( selector, time, callback ) {
  const element = getEl( selector );
  element.style.transition = 'opacity ' + time + 'ms ease-in-out';
  element.style.opacity = 0.05;
  element.style.display = 'block';

  window.setTimeout( function( ) {
    return ( element.style.opacity = 1 );
  }, 100 );

  window.setTimeout( function( ) {
    element.style.display = 'block';
    return ( callback || NO_OP )( );
  }, time );
}

/**
 * @param {string} selector - Selector for an element.
 * @param {number} time - When to call the callback.
 * @param {[Function]} callback - Function to call after delay.
 */
function fadeOut( selector, time, callback ) {
  const element = getEl( selector );
  element.style.transition = 'opacity ' + time + 'ms ease-in-out';
  element.style.opacity = 1;

  window.setTimeout( function( ) {
    return ( element.style.opacity = 0.05 );
  }, 100 );

  window.setTimeout( function( ) {
    element.style.display = 'none';
    return ( callback || NO_OP )( );
  }, time );
}

function mutate( callback ) {
  _mutate( callback );
}

function nextFrame( callback ) {
  fastDom.raf( callback );
}

export default {
  applyAll,
  bindEvents,
  addEl,
  getElData,
  changeElText,
  changeElHTML,
  createEl,
  removeEl,
  addClass,
  hasClass,
  removeClass,
  toggleClass,
  filter,
  getEl,
  getEls,
  getChildEls,
  getParentEls,
  getPreviousEls,
  getNextEls,
  isEl,
  hide,
  show,
  fadeIn,
  fadeOut,
  mutate,
  nextFrame
};
