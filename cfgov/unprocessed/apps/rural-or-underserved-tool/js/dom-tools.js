import fastDom from 'fastdom';

const NO_OP = function NO_OP() {
  // Placeholder function meant to be overridden.
};

const _matches = (function _getMatches() {
  const el = document.body;
  return (
    el.matches ||
    el.webkitMatchesSelector ||
    el.mozMatchesSelector ||
    el.msMatchesSelector
  );
})();

/**
 * @param {string} selector - A CSS selector.
 * @param {Function} callback - Function to call on queried element.
 */
function _mutate(selector, callback) {
  applyAll(selector, function (element) {
    fastDom.mutate(callback.bind(null, element));
  });
}

/* Code copied from jQuery with minimal modifications.
   XHTML parsers do not magically insert elements in the
   same way that tag soup parsers do. So we cannot shorten
   this by omitting <tbody> or other required elements. */
const _firstTag = /<([a-z][^/\0>\x20\t\r\n\f]+)/;
const _wrapMap = {
  col: [2, '<table><colgroup>', '</colgroup></table>'],
  default: [0, '', ''],
  option: [1, "<select multiple='multiple'>", '</select>'],
  td: [3, '<table><tbody><tr>', '</tr></tbody></table>'],
  thead: [1, '<table>', '</table>'],
  tr: [2, '<table><tbody>', '</tbody></table>'],
};

/**
 * @param {HTMLElement|string} elements - An HTML element or a selector.
 * @param {Function} applyFn - Function to apply to each element.
 */
function applyAll(elements, applyFn) {
  if (elements instanceof HTMLElement) {
    elements = [elements];
  } else if (typeof elements === 'string') {
    elements = getEls(elements);
  }

  return [].slice.call(elements || []).forEach(applyFn);
}

/**
 * @param {Array} elements - A list of HTML DOM nodes.
 * @param {Array|string} events - A list or single event type.
 * @param {Function} callback - A function to call at the end.
 */
function bindEvents(elements, events, callback) {
  if (Array.isArray(events) === false) {
    events = [events];
  }

  applyAll(elements, function (element) {
    events.forEach(function (event) {
      element.addEventListener(event, callback || NO_OP);
    });
  });
}

/**
 * @param {HTMLElement|string} parent - An HTML element node or CSS selector.
 * @param {HTMLElement|string} child - An HTML element node or snippet.
 */
function addEl(parent, child) {
  return fastDom.mutate(function () {
    const el = createEl(child);
    return getEl(parent).appendChild(el);
  });
}

/**
 * @param {string} selector - A CSS selector.
 * @param {string} attributeName - A value to add to a data- attribute.
 */
function getElData(selector, attributeName) {
  return getEl(selector).getAttribute('data-' + attributeName);
}

/**
 * @param {string} selector - A CSS selector.
 * @param {string} text - Some text content.
 */
function changeElText(selector, text) {
  _mutate(selector, function (element) {
    return (element.textContent = text);
  });
}

/**
 * @param {string} selector - A CSS selector.
 * @param {string} HTML - An HTML snippet.
 */
function changeElHTML(selector, HTML) {
  _mutate(selector, function (element) {
    return (element.innerHTML = HTML);
  });
}

/**
 * @param {HTMLElement} element - An element.
 * @param {string} filterNode - The string to filter by.
 */
function getNextEls(element, filterNode) {
  return _filter(element, 'nextElementSibling', filterNode);
}

/**
 * Code copied from jQuery with minimal modifications.
 * @param {HTMLElement|string} HTML - An HTML DOM node or snippet.
 * @returns {DocumentFragment} The created document fragment node.
 */
function createEl(HTML) {
  if (_isEl(HTML)) {
    return HTML;
  }
  let container = document.createElement('div');
  const tag = (_firstTag.exec(HTML) || ['', ''])[1].toLowerCase();
  const elWrapper = _wrapMap[tag] || _wrapMap.default;
  const docFrag = document.createDocumentFragment();
  container.innerHTML = elWrapper[1] + HTML + elWrapper[2];
  let wrapperCount = elWrapper[0];
  while (wrapperCount--) {
    container = container.firstChild;
  }

  [].slice.call(container.childNodes).forEach(function (node) {
    docFrag.appendChild(node);
  });

  return docFrag;
}

/**
 * @param {string} selector - A CSS selector.
 */
function removeEl(selector) {
  _mutate(selector, function (element) {
    return element.parentNode.removeChild(element);
  });
}

/**
 * @param {string} selector - A CSS selector.
 * @param {string} className - A CSS class to remove.
 */
function addClass(selector, className) {
  _mutate(selector, function (element) {
    const _classList = element.classList;
    return _classList.add(className);
  });
}

/**
 * @param {string} selector - A CSS selector.
 * @param {string} className - A CSS class to remove.
 * @returns {boolean} True if the element has the CSS class, false otherwise.
 */
function hasClass(selector, className) {
  let _hasClass = false;
  applyAll(selector, function (element) {
    if (element.classList.contains(className)) {
      _hasClass = true;
    }
  });
  return _hasClass;
}

/**
 * @param {string} selector - A CSS selector.
 * @param {string} className - A CSS class to remove.
 */
function removeClass(selector, className) {
  _mutate(selector, function (element) {
    const _classList = element.classList;
    return _classList.remove(className);
  });
}

/**
 * @param {HTMLElement} element - An element.
 * @param {string} propName - An HTML element property to select for.
 * @param {string} filter - The string to filter by.
 */
function _filter(element, propName, filter) {
  const _propName = propName || '';
  const _filter = filter || '*';

  const nodes = [];
  let node = element[_propName];

  while (node && node !== document) {
    if (_matches.call(node, _filter)) {
      nodes.push(node);
    }
    node = node[_propName];
  }
  return nodes;
}

/**
 * @param {HTMLElement|string} selector - An HTML element node or CSS selector.
 * @returns {HTMLElement} An HTML node returned by the passed selector,
 *  or the selector passed into this method.
 */
function getEl(selector) {
  if (_isEl(selector)) {
    return selector;
  }
  return document.querySelector(selector);
}

/**
 * @param {HTMLElement|string} selector - An HTML element node or CSS selector.
 * @returns {NodeList} A list of HTML nodes returned by the passed selector,
 *  or the selector passed into this method.
 */
function getEls(selector) {
  if (_isEl(selector)) {
    return selector;
  }
  return document.querySelectorAll(selector);
}

/**
 * @param {HTMLElement} element - An element.
 * @param {string} filterNode - The string to filter by.
 */
function getParentEls(element, filterNode) {
  return _filter(element, 'parentNode', filterNode);
}

/**
 * Check whether something is a NodeList, HTML element, or window.
 * @param {*} element - An object to check for element-ness.
 */
function _isEl(element) {
  return (
    element instanceof NodeList ||
    element instanceof HTMLElement ||
    element instanceof DocumentFragment ||
    element instanceof Window
  );
}

/**
 * @param {Function} callback - Function to pass to the wrapped call
 *   to requestAnimationFrame.
 */
function nextFrame(callback) {
  fastDom.raf(callback);
}

export {
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
  getEl,
  getEls,
  getParentEls,
  getNextEls,
  nextFrame,
};
