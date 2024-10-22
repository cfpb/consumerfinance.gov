/**
 * @param {Document|Window|string} selector - A jQuery-style selector.
 * @returns {Document|Window|undefined} The Query object.
 */
function Query(selector) {
  this.elements = [];

  if (typeof selector === 'undefined') {
    return this;
  }

  if (selector.nodeType) {
    this.elements[0] = selector;

    return this;
  }

  this.selector = selector;

  // handle :last jquery selector
  if (selector.indexOf(':last') !== -1) {
    selector = selector.split(':')[0];
    const arr = document.querySelectorAll(selector);
    this.elements = arr.length ? [arr[arr.length - 1]] : [];
    this.selector = selector;

    return this;
  }

  // handle :selected jquery selector
  if (selector.indexOf(':selected') !== -1) {
    selector = selector.split(':')[0];
    const arr = document.querySelector(selector);
    const parent = arr.parentElement;

    this.elements.push(parent.options[parent.selectedIndex]);
    this.selector = selector;

    return this;
  }

  if (selector === document) {
    this.elements.push(document);
  } else if (selector === '$WINDOW') {
    this.elements.push(document.defaultView);
  } else if (typeof selector === 'string' && selector !== '') {
    this.elements = document.querySelectorAll(selector);
  }

  return this;
}

/**************************/
// Helper functions
/**************************/

/**
 * Turns a number into a string ending with 'px'
 * @param {number} val - numeric value
 * @returns {string} string ending with 'px'
 */
function pixelator(val) {
  if (typeof val === 'number') {
    return val.toString() + 'px';
  } else if (typeof val === 'string') {
    return val.replace(/\D/g, '') + 'px';
  }

  return '0px';
}

/**************************/
// Reference variables
/**************************/

const pixelStyles = ['width', 'height', 'left', 'right', 'top', 'bottom'];

const slideUpVars = {
  styles: {
    transitionProperty: 'height, margin, padding',
    boxSizing: 'border-box',
    overflow: 'hidden',
    height: 0,
    paddingTop: 0,
    paddingBottom: 0,
    marginTop: 0,
    marginBottom: 0,
  },
  removals: [
    'height',
    'padding-top',
    'padding-bottom',
    'margin-top',
    'margin-bottom',
    'overflow',
    'transition-duration',
    'transition-property',
  ],
};

const slideDownVars = {
  styles: {
    overflow: 'hidden',
    height: 0,
    paddingTop: 0,
    paddingBottom: 0,
    marginTop: 0,
    marginBottom: 0,
    boxSizing: 'border-box',
    transitionProperty: 'height, margin, padding',
  },
  removals: ['padding-top', 'padding-bottom', 'margin-top', 'margin-bottom'],
  delayedRemovals: [
    'height',
    'overflow',
    'transition-duration',
    'transition-property',
  ],
};

/**************************/
// Object elements[] helpers
/**************************/

Query.prototype.each = function (callback) {
  this.elements.forEach(function (elem, index) {
    callback.call(elem, elem, index);
  });
};

Query.prototype.find = function (findSelector) {
  if (typeof this.selector !== 'undefined') {
    return new Query(this.selector + ' ' + findSelector);
  } else {
    const q = new Query();
    const elemArr = [];
    this.elements.forEach((elem) => {
      elem.querySelectorAll(findSelector).forEach((elem) => {
        elemArr.push(elem);
      });
    });
    q.elements = elemArr;

    return q;
  }
};

Query.prototype.closest = function (closestSelector) {
  if (typeof closestSelector === 'undefined' || this.elements.length < 1)
    return this;
  const q = new Query();
  const elemArr = [];
  elemArr.push(this.elements[0].closest(closestSelector));
  q.elements = elemArr;

  return q;
};

Query.prototype.not = function (notSelector) {
  if (typeof this.selector !== 'undefined') {
    return new Query(this.selector + ':not(' + notSelector + ')');
  } else {
    const q = new Query();
    const elemArr = [];
    this.elements.forEach((elem) => {
      if (!elem.matches(notSelector)) {
        elemArr.push(elem);
      }
    });
    q.elements = elemArr;

    return q;
  }
};

Query.prototype.filter = function (selector) {
  return new Query(this.selector + '' + selector);
};

Query.prototype.siblings = function (selector) {
  const q = new Query();
  const elemArr = [];
  if (typeof selector === 'undefined') selector = '*';
  this.elements.forEach((elem) => {
    let node = elem.parentNode.firstElementChild;
    for (node; node !== null; node = node.nextElementSibling) {
      if (node.matches(selector) && node !== elem) {
        elemArr.push(node);
      }
    }
  });
  q.elements = elemArr;

  return q;
};

Query.prototype.parent = function (selector) {
  const q = new Query();
  const elemArr = [];
  this.elements.forEach((elem) => {
    const parent = elem.parentElement;
    if (typeof selector === 'undefined' || parent.matches(selector)) {
      elemArr.push(parent);
    }
  });

  q.elements = elemArr;

  return q;
};

Query.prototype.remove = function () {
  this.elements.forEach((elem) => {
    elem.remove();
  });

  return this;
};

/**************************/
// DOM element text, value
/**************************/

Query.prototype.text = function (value) {
  // getter
  if (typeof value === 'undefined') {
    return this.elements.length ? this.elements[0].textContent : null;
  }
  //setter
  else {
    this.elements.forEach((elem) => {
      elem.textContent = value;
    });

    return this;
  }
};

Query.prototype.html = function (value) {
  //getter
  if (typeof value === 'undefined') {
    return this.elements.length ? this.elements[0].innerHTML : null;
  }
  //setter
  else {
    this.elements.forEach((elem) => {
      elem.innerHTML = value;
    });

    return this;
  }
};

Query.prototype.val = function (value) {
  // getter
  if (typeof value === 'undefined' && this.elements.length > 0) {
    return this.elements.length ? this.elements[0].value : null;
  }
  //setter
  else {
    this.elements.forEach((elem) => {
      elem.value = value;
    });
    return this;
  }
};

/**************************/
// event listeners and triggers
/**************************/
Query.prototype.listen = function (eventType, callback) {
  this.elements.forEach((elmo) => {
    elmo.addEventListener(eventType, callback);
  });
};

Query.prototype.click = function (callback) {
  this.listen('click', callback);
};

Query.prototype.submit = function (callback) {
  this.listen('submit', callback);
};

/**
 * Handles events in eventType
 * @param {string} eventType - Type of event for which to listen
 * @param {string | Function} paramOne - A selector or callback
 * @param {Function} paramTwo - A callback if paramOne is a selector.
 * @returns {object} this Query object
 */
Query.prototype.on = function (eventType, paramOne, paramTwo) {
  if (typeof paramOne == 'function') {
    this.elements.forEach((elem) => {
      eventType.split(' ').forEach((type) => {
        elem.addEventListener(type, paramOne);
      });
    });
  } else {
    this.elements.forEach((elem) => {
      const callback = function (ev) {
        if (!ev.target) return;
        const elem = ev.target.closest(paramOne);
        if (elem) {
          paramTwo.call(elem, ev);
        }
      };
      eventType.split(' ').forEach((type) => {
        elem.addEventListener(type, callback);
      });
      return callback;
    });
  }

  return this;
};

Query.prototype.blur = function () {
  this.elements.forEach((elem) => {
    elem.blur();
  });
};

Query.prototype.change = function () {
  this.elements.forEach((elem) => {
    if (elem.tagName === 'SELECT') {
      const change = new Event('change');
      change.currentTarget = elem;
      elem.dispatchEvent(change);
    }
  });
};

Query.prototype.keypress = function (callback) {
  this.listen('keyup', callback);
};

Query.prototype.keyup = function (callback) {
  this.listen('keyup', callback);
};

Query.prototype.resize = function (callback) {
  document.defaultView.addEventListener('resize', callback);
};

/**************************/
// classes, styles, attributes, and properties
/**************************/

Query.prototype.tagName = function () {
  return this.elements.length ? this.elements[0].tagName : null;
};

Query.prototype.addClass = function (classNames) {
  const classArr = classNames.split(' ');
  this.elements.forEach((elem) => {
    elem.classList.add(...classArr);
  });

  return this;
};

Query.prototype.removeClass = function (classNames) {
  const classArr = classNames.split(' ');
  this.elements.forEach((elem) => {
    elem.classList.remove(...classArr);
  });

  return this;
};

Query.prototype.attr = function (name, value) {
  if (typeof value === 'undefined') {
    return this.elements.length ? this.elements[0].getAttribute(name) : null;
  } else if (value === false) {
    this.elements.forEach((elem) => {
      elem.removeAttribute(name);
    });
  } else {
    if (this.elements.length < 1) return this;
    this.elements.forEach((elem) => {
      elem.setAttribute(name, value);
    });
  }

  return this;
};

Query.prototype.is = function (selector) {
  if (typeof selector === 'string') {
    return this.elements.length ? this.elements[0].matches(selector) : this;
  }

  return this;
};

Query.prototype.hide = function () {
  this.elements.forEach((elem) => {
    elem.style.display = 'none';
  });

  return this;
};

Query.prototype.show = function (className) {
  this.elements.forEach((elem) => {
    if (typeof className !== 'undefined') {
      elem.style.display = className;
    } else {
      elem.style.display = 'block';
    }
  });

  return this;
};

Query.prototype.slideUp = function (duration = 500) {
  this.elements.forEach((elem) => {
    elem.style.transitionDuration = duration + 'ms';
    for (const key in slideUpVars.styles) {
      elem.style[key] = slideUpVars.styles[key];
    }
    elem.style.height = elem.offsetHeight + 'px';
    void elem.offsetWidth;
    document.defaultView.setTimeout(() => {
      slideUpVars.removals.forEach((item) => {
        elem.style.removeProperty(item);
      });
      elem.style.display = 'none';
    }, duration);
  });

  return this;
};

Query.prototype.slideDown = function (duration = 500) {
  this.elements.forEach((elem) => {
    elem.style.removeProperty('display');
    let display = document.defaultView.getComputedStyle(elem).display;
    if (display === 'none') display = 'block';
    elem.style.display = display;
    const height = elem.offsetHeight;
    for (const key in slideDownVars.styles) {
      elem.style[key] = slideDownVars.styles[key];
    }
    void elem.offsetWidth;
    elem.style.transitionDuration = duration + 'ms';
    elem.style.height = height + 'px';
    slideDownVars.removals.forEach((item) => {
      elem.style.removeProperty(item);
    });
    document.defaultView.setTimeout(() => {
      slideDownVars.delayedRemovals.forEach((item) => {
        elem.style.removeProperty(item);
      });
    });
  });

  return this;
};

Query.prototype.height = function (val) {
  if (typeof val === 'undefined') {
    if (this.elements.length > 0) {
      const elem = this.elements[0];
      if (Object.prototype.hasOwnProperty.call(elem, 'getBoundingClientRect')) {
        return elem.getBoundingClientRect().height;
      }
      return this.elements[0].offsetHeight;
    }
    return null;
  } else {
    this.elements.forEach((elem) => {
      if (typeof val === 'function') {
        val = val();
      } else {
        if (typeof val !== 'string') {
          val += 'px';
        }
        elem.style.height = val;
      }
    });

    return this;
  }
};

Query.prototype.outerHeight = function (val) {
  if (typeof val === 'undefined') {
    return this.elements.length ? this.elements[0].offsetHeight : null;
  } else {
    this.elements.forEach((elem) => {
      if (typeof val === 'function') {
        val = val();
      } else {
        if (typeof val !== 'string') {
          val += 'px';
        }
        elem.style.height = val;
      }
    });

    return this;
  }
};

Query.prototype.top = function () {
  return this.elements.length ? this.elements[0].offsetTop : null;
};

Query.prototype.width = function (val) {
  if (typeof val === 'undefined') {
    if (this.elements.length < 1) return this;
    const elem = this.elements[0];
    if (elem.window === elem) {
      return document.defaultView.outerWidth;
    } else {
      return elem.getBoundingClientRect().width;
    }
  } else {
    if (typeof val === 'function') {
      val = val();
    } else {
      if (this.elements.length < 1) return this;
      if (typeof val !== 'string') val = val + 'px';
      this.elements.forEach((elem) => {
        elem.style.width = val;
      });
    }
  }
};

Query.prototype.outerWidth = function (val) {
  if (this.elements.length < 1) return this;
  const elem = this.elements[0];
  if (val === true) {
    const style = getComputedStyle(elem);
    return (
      elem.getBoundingClientRect().width +
      parseFloat(style.marginLeft) +
      parseFloat(style.marginRight)
    );
  } else {
    return elem.offsetWidth;
  }
};

Query.prototype.scrollTop = function (val) {
  if (typeof val === 'undefined') {
    const elem = this.elements[0];
    if (elem) {
      if (elem.window === elem) {
        return document.defaultView.pageYOffset;
      } else {
        return elem.scrollTop;
      }
    }
  } else {
    this.elements.forEach((elem) => {
      if (elem.window === elem) {
        const xOff = document.defaultView.pageXOffset;
        document.defaultView.scrollTo(xOff, val);
      } else {
        elem.scrollTop = val;
      }
    });
  }
};

Query.prototype.offset = function () {
  if (this.elements.length < 1) return this;
  const elem = this.elements[0];
  const win = document.defaultView;
  const bound = elem.getBoundingClientRect();
  const docTop = document.documentElement.clientTop;
  const docLeft = document.documentElement.clientLeft;
  return {
    top: bound.top + win.pageYOffset + docTop,
    left: bound.left + win.pageXOffset + docLeft,
  };
};

Query.prototype.css = function (param, value) {
  if (this.elements.length < 1) return this;
  let obj = {};
  if (typeof param !== 'object' && typeof value === 'undefined') {
    const styles = getComputedStyle(this.elements[0]);
    return styles[param];
  } else if (typeof param !== 'object') {
    obj[param] = value;
  } else {
    obj = param;
  }
  for (const key in obj) {
    this.elements.forEach((elem) => {
      if (Object.prototype.hasOwnProperty.call(elem.style, key)) {
        let val = obj[key];
        if (pixelStyles.indexOf(key) > -1) val = pixelator(val);
        elem.style[key] = val;
      }
    });
  }
  return this;
};

/**************************/
// DOM manipulation
/**************************/

Query.prototype.cloner = function () {
  return this.elements.length ? this.elements[0].cloneNode(true) : null;
};

Query.prototype.append = function (elem) {
  this.elements.forEach((parent) => {
    if (typeof elem === 'string') {
      parent.innerHTML += elem;
    } else {
      parent.append(elem);
    }
  });

  return this;
};

Query.prototype.appendTo = function (newParents) {
  // This method is designed only to work on instances of Query
  if (newParents instanceof Query !== true) {
    throw Error(
      'Error: appendTo can only accept an instance of Query as a parameter',
    );
  } else {
    newParents.elements.forEach((parent) => {
      this.elements.forEach((child) => {
        parent.appendChild(child);
      });
    });
  }

  return this;
};

Query.prototype.empty = function () {
  this.elements.forEach((elem) => {
    elem.replaceChildren();
  });
};

// Constructor function
const $ = function (param) {
  if (typeof param === 'string') {
    return new Query(param);
  } else if (typeof param === 'object') {
    if (param.nodeType) {
      const q = new Query();
      q.elements = [param];
      return q;
    } else {
      const q = new Query();
      this.elements = param;
      return q;
    }
  }
};

$.each = function (obj, callback) {
  obj.forEach(function (elem, index) {
    // This is an odd reversal of parameters, but matches jQuery.each()
    callback(index, elem);
  }, obj);
};

export const window = '$WINDOW';

export default $;
