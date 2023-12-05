/**
 * @param {Document|Window|string} selector - A jQuery-style selector.
 * @returns {Document|Window|undefined} The document, window, or nothing.
 */
function Query(selector) {
  this.elements = [];

  if (selector === document) {
    return document;
  }

  if (selector === window) {
    return window;
  }

  this.selector = selector;
  if (typeof selector === 'string' && selector !== '') {
    this.elements = document.querySelectorAll(selector);
  }
}

Query.prototype.attr = function (name, value) {
  if (typeof value === 'undefined') {
    return this.elements.length ? this.elements[0].getAttribute(name) : null;
  } else {
    this.elements.forEach((elem) => {
      elem.setAttribute(name, value);
    });
  }
};

Query.prototype.cloner = function () {
  return this.elements.length ? this.elements[0].cloneNode(true) : null;
};

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

Query.prototype.each = function (callback) {
  this.elements.forEach((elem, index) => {
    callback(elem, index);
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

Query.prototype.remove = function () {
  this.elements.forEach((elem) => {
    elem.remove();
  });
};

Query.prototype.hide = function () {
  this.elements.forEach((elem) => {
    elem.style.display = 'none';
  });
};

Query.prototype.show = function (className) {
  this.elements.forEach((elem) => {
    if (typeof className !== 'undefined') {
      elem.style.display = className;
    } else {
      elem.style.display = 'block';
    }
  });
};

Query.prototype.height = function () {
  return this.elements.length ? this.elements[0].offsetHeight : null;
};

Query.prototype.top = function () {
  return this.elements.length ? this.elements[0].offsetTop : null;
};

Query.prototype.listen = function (eventType, callback) {
  this.elements.forEach((elmo) => {
    elmo.addEventListener(eventType, callback);
  });
};

Query.prototype.tagName = function () {
  return this.elements.length ? this.elements[0].tagName : null;
};

Query.prototype.addClass = function (classNames) {
  const classArr = classNames.split(' ');
  this.elements.forEach((elem) => {
    elem.classList.add(...classArr);
  });
};

Query.prototype.removeClass = function (classNames) {
  const classArr = classNames.split(' ');
  this.elements.forEach((elem) => {
    elem.classList.remove(...classArr);
  });
};

Query.prototype.change = function () {
  this.elements.forEach((elem) => {
    if (elem.tagName === 'SELECT') {
      elem.dispatchEvent(new Event('change'));
    }
  });
};

const $ = function (param) {
  if (typeof param === 'string') {
    return new Query(param);
  } else if (typeof param === 'object') {
    if (typeof param.length === 'undefined') {
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

export default $;
