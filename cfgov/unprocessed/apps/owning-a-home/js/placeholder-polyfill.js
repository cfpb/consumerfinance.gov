//
// HTML5 Placeholder Attribute Polyfill (Simple)
//
// Author: James Brumond <james@jbrumond.me> (http://www.jbrumond.me)
//
// https://github.com/jamesallardice/Placeholders.js

(function(window, document, undefined) {

  // Don't run the polyfill if it isn't needed
  if ('placeholder' in document.createElement('input')) {
    document.placeholderPolyfill = function() { /*  no-op */ };
    document.placeholderPolyfill.active = false;
    return;
  }

  // Fetch NodeLists of the needed element types
  var inputs = document.getElementsByTagName('input');
  var textareas = document.getElementsByTagName('textarea');

  //
  // Define the exposed polyfill methods for manual calls
  //
  document.placeholderPolyfill = function(elems) {
    elems = elems ? validElements(elems) : validElements(inputs, textareas);
    each(elems, polyfillElement);
  };

  // Expose whether or not the polyfill is in use (false means native support)
  document.placeholderPolyfill.active = true;

  // Run automatically
  document.placeholderPolyfill();

// -------------------------------------------------------------

  // Use mutation events for auto-updating
  if (document.addEventListener) {
    document.addEventListener('DOMAttrModified', document.placeholderPolyfill);
    document.addEventListener('DOMNodeInserted', document.placeholderPolyfill);
  }

  // Use onpropertychange for auto-updating
  else if (document.attachEvent && 'onpropertychange' in document) {
    document.attachEvent('onpropertychange', document.placeholderPolyfill);
  }

  // No event-based auto-update
  else {
    // pass
  }

// -------------------------------------------------------------

  // Add some basic default styling for placeholders
  firstStylesheet().addRule('.-placeholder', 'color: #888;', 0);

// -------------------------------------------------------------

  //
  // Polyfill a single, specific element
  //
  function polyfillElement(elem) {
    // If the element is already polyfilled, skip it
    if (elem.__placeholder != null) {
      // Make sure that if the placeholder is already shown, that it is at least up-to-date
      if (elem.__placeholder) {
        elem.value = getPlaceholder();
      }
      return;
    }

    // Keep track of placeholder changes so we can fire off updates correctly
    var currentPlaceholder = getPlaceholderFor(elem);
    function getPlaceholder() {
      return currentPlaceholder = getPlaceholderFor(elem);
    }

    // Is there already a value in the field? If so, don't replace it with the placeholder
    if (elem.value) {
      elem.__placeholder = false;
      if (elem.value === getPlaceholder()) {
        doShowPlaceholder();
      }
    } else {
      showPlaceholder();
    }

    // Define the events that cause these functions to be fired
    addEvent(elem, 'keyup',    checkPlaceholder);
    addEvent(elem, 'keyDown',  checkPlaceholder);
    addEvent(elem, 'blur',     checkPlaceholder);
    addEvent(elem, 'focus',    hidePlaceholder);
    addEvent(elem, 'click',    hidePlaceholder);

    // Use mutation events for auto-updating
    if (elem.addEventListener) {
      addEvent(elem, 'DOMAttrModified', updatePlaceholder);
    }

    // Use onpropertychange for auto-updating
    else if (elem.attachEvent && 'onpropertychange' in elem) {
      addEvent(elem, 'propertychange', updatePlaceholder);
    }

    // No event-based auto-update
    else {
      // pass
    }

    function updatePlaceholder() {
      // Run this asynchronously to make sure all needed updates happen before we run checks
      setTimeout(function() {
        var old = currentPlaceholder;
        var current = getPlaceholder();

        // If the placeholder attribute has changed
        if (old !== current) {
          // If the placeholder is currently shown
          if (elem.__placeholder) {
            elem.value = current;
          }
        }

        // Make sure that elem.__placeholder stays acurate, even if the placeholder or value are
        // manually changed via JavaScript
        if (elem.__placeholder && elem.value !== current) {
          elem.__placeholder = false;
        }
      }, 0);
    }

    function checkPlaceholder() {
      if (elem.value) {
        hidePlaceholder();
      } else {
        showPlaceholder();
      }
    }

    function showPlaceholder() {
      if (! elem.__placeholder && ! elem.value) {
        doShowPlaceholder();
      }
    }

    function doShowPlaceholder() {
      elem.__placeholder = true;
      elem.value = getPlaceholder();
      addClass(elem, '-placeholder');
    }

    function hidePlaceholder() {
      if (elem.__placeholder) {
        elem.__placeholder = false;
        elem.value = '';
        removeClass(elem, '-placeholder');
      }
    }
  }

// -------------------------------------------------------------

  //
  // Build a list of valid (can have a placeholder) elements from the given parameters
  //
  function validElements() {
    var result = [ ];

    each(arguments, function(arg) {
      if (typeof arg.length !== 'number') {
        arg = [ arg ];
      }

      result.push.apply(result, filter(arg, isValidElement));
    });

    return result;
  }

  //
  // Check if a given element supports the placeholder attribute
  //
  function isValidElement(elem) {
    var tag = (elem.nodeName || '').toLowerCase();
    return (tag === 'textarea' || (tag === 'input' && (elem.type === 'text' || elem.type === 'password')));
  }

// -------------------------------------------------------------

  function addEvent(obj, event, func) {
    if (obj.addEventListener) {
      obj.addEventListener(event, func, false);
    } else if (obj.attachEvent) {
      obj.attachEvent('on' + event, func);
    }
  }

  function removeEvent(obj, event, func) {
    if (obj.removeEventListener) {
      obj.removeEventListener(event, func, false);
    } else if (obj.detachEvent) {
      obj.detachEvent('on' + event, func);
    }
  }

// -------------------------------------------------------------

  function each(arr, func) {
    if (arr.forEach) {
      return arr.forEach(func);
    }

    for (var i = 0, c = arr.length; i < c; i++) {
      func.call(null, arr[i], i, arr);
    }
  }

  function filter(arr, func) {
    if (arr.filter) {
      return arr.filter(func);
    }

    var result = [ ];
    for (var i = 0, c = arr.length; i < c; i++) {
      if (func.call(null, arr[i], i, arr)) {
        result.push(arr[i]);
      }
    }

    return result;
  }

// -------------------------------------------------------------

  var regexCache = { };
  function classNameRegex(cn) {
    if (! regexCache[cn]) {
      regexCache[cn] = new RegExp('(^|\\s)+' + cn + '(\\s|$)+', 'g');
    }

    return regexCache[cn];
  }

  function addClass(elem, cn) {
    elem.className += ' ' + cn;
  }

  function removeClass(elem, cn) {
    elem.className = elem.className.replace(classNameRegex(cn), ' ');
  }

// -------------------------------------------------------------

  // Internet Explorer 10 in IE7 mode was giving me the weirdest error
  // where e.getAttribute('placeholder') !== e.attributes.placeholder.nodeValue
  function getPlaceholderFor(elem) {
    return elem.getAttribute('placeholder') || (elem.attributes.placeholder && elem.attributes.placeholder.nodeValue);
  }

// -------------------------------------------------------------

  // Get the first stylesheet in the document, or, if there are none, create/inject
  // one and return it.
  function firstStylesheet() {
    var sheet = document.styleSheets && document.styleSheets[0];
    if (! sheet) {
      var head = document.head || document.getElementsByTagName('head')[0];
      var style = document.createElement('style');
      style.appendChild(document.createTextNode(''));
      document.head.appendChild(style);
      sheet = style.sheet;
    }
    return sheet;
  }

}(window, document));
