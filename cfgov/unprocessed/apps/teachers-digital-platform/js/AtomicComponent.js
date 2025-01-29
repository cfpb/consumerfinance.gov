// TODO: Note that this is an older copy of AtomicComponent from the
// design-system to isolate TDP expandable customizations.

/* ==========================================================================
   AtomicComponent
   Base Atomic Component
   Contains code copied from the following with major modifications :
   - Backbone.js ( http://backbonejs.org/docs/backbone.html ).
   - Marionette ( http://marionettejs.com ).
   ========================================================================== */

import {
  isFunction,
  EventObserver,
  instantiateAll,
  setInitFlag,
} from '@cfpb/cfpb-design-system';
import Delegate from 'ftdomdelegate';

const TAG_NAME = 'div';

/**
 * Function as the constrcutor for the AtomicComponent.
 * Sets up initial instance properties and calls
 * necessary methods to properly instantiatie component.
 * @param {HTMLElement} element - The element to set as the base element.
 * @param {object} attributes - Hash of attributes to set on base element.
 */
function AtomicComponent(element, attributes) {
  this.element = element;
  this.initializers = [];
  this.uId = this.uniqueId('ac');
  Object.assign(this, attributes);
  this.processModifiers();
  this.ensureElement();
  this.setCachedElements();
  this.initializers.push(this.initialize);
}

// Public instance Methods and properties.
Object.assign(AtomicComponent.prototype, new EventObserver(), {
  /**
   * Run through and call the component's initializers.
   * @returns {AtomicComponent} An instance.
   */
  init: function () {
    this.initializers.forEach(function (func) {
      if (isFunction(func)) {
        func.apply(this, arguments);
      }
    }, this);
    this.dispatchEvent('component:initialized');

    return this;
  },

  /**
   * Function used to process class modifiers. These should
   * correspond with BEM modifiers.
   */
  processModifiers: function () {
    if (!this.modifiers) {
      return;
    }

    this.modifiers.forEach(function (modifier) {
      const modifierClass = modifier.ui.base.substring(1);
      if (this.element.classList.contains(modifierClass)) {
        if (modifier.initialize) {
          this.initializers.push(modifier.initialize);
        }
        Object.assign(this, modifier);
      }
    }, this);
  },

  /**
   * Function used to render a template in Single Page Applications.
   * @returns {AtomicComponent} An instance.
   */
  render: function () {
    return this;
  },

  /**
   * Function used to ensure and set / create the base DOM element.
   */
  ensureElement: function () {
    if (!this.element) {
      const attrs = Object.assign({}, this.attributes);
      attrs.id = this.id || this.u_id;
      if (this.className) attrs.class = this.className;
      this.setElement(document.createElement(TAG_NAME));
      this.setElementAttributes(attrs);
    } else {
      this.setElement(this.element);
    }
    setInitFlag(this.element);
  },

  /**
   * Function used to set the base DOM element.
   * @param {HTMLElement} element - The element to set as the base element.
   * @returns {AtomicComponent} An instance.
   */
  setElement: function (element) {
    if (this.element) {
      this.undelegateEvents();
    }
    this.element = element;
    this.delegateEvents();

    return this;
  },

  // TODO Fix complexity issue

  /**
   * Function used to set the cached DOM elements.
   * @returns {object} Hash of event names and cached elements.
   */
  setCachedElements: function () {
    const ui = Object.assign({}, this.ui);
    let key;
    let element;

    for (key in ui) {
      if ({}.hasOwnProperty.call(ui, key)) {
        element = this.element.querySelectorAll(ui[key]);
        if (element.length === 1) {
          ui[key] = element[0];
        } else if (element.length > 1) {
          ui[key] = element;
        } else {
          ui[key] = null;
        }
      }
    }
    this.ui = ui;

    return ui;
  },

  /**
   * Function used to remove the base element from the DOM
   * and unbind events.
   * @returns {boolean} True if successful in tearing down component.
   */
  destroy: function () {
    if (this.element) {
      this.element.parentNode.removeChild(this.element);
      if (this.element.view) delete this.element.view;
      delete this.element;
    }
    this.undelegateEvents();
    this.dispatchEvent('component:destroyed');

    return true;
  },

  /**
   * Function used to set the attributes on an element.
   * @param {object} attributes - Hash of attributes to set on base element.
   */
  setElementAttributes: function (attributes) {
    let property;

    for (property in attributes) {
      if ({}.hasOwnProperty.call(attributes, property)) {
        this.element.setAttribute(property, attributes[property]);
      }
    }
  },

  // TODO Fix complexity issue

  /**
   * Function used to up event delegation on the base element.
   * Using Dom-delegate library to enable this functionality.
   * @param {object} events - Hash of events to bind to the dom element.
   * @returns {AtomicComponent} An instance.
   */
  delegateEvents: function (events) {
    const delegateEventSplitter = /^(\S+)\s*(.*)$/;
    let key;
    let method;
    let match;

    events = events || (events = this.events);
    if (!events) {
      return this;
    }

    this.undelegateEvents();
    this._delegate = new Delegate(this.element);
    for (key in events) {
      if ({}.hasOwnProperty.call(events, key)) {
        method = events[key];
        if (isFunction(this[method])) {
          method = this[method];
        }
        if (method) {
          match = key.match(delegateEventSplitter);
          this.delegate(match[1], match[2], method.bind(this));
        }
      }
    }
    this.dispatchEvent('component:bound');

    return this;
  },

  /**
   * Function used to set the attributes on an element.
   * @param {string} eventName - Event in which to listen for.
   * @param {string} selector - CSS selector.
   * @param {Function} listener - Callback for event.
   * @returns {AtomicComponent} An instance.
   */
  delegate: function (eventName, selector, listener) {
    this._delegate.on(eventName, selector, listener);

    return this;
  },

  /**
   * Function used to remove events from the base element.
   * @returns {AtomicComponent} An instance.
   */
  undelegateEvents: function () {
    if (this._delegate) {
      this._delegate.destroy();
    }
    this.element.removeAttribute('data-js-hook');

    return this;
  },

  /**
   * Function used to set the attributes on an element.
   * @param {string} prefix - String to use a prefix.
   * @returns {string} Prefixed unique id string.
   */
  uniqueId: function (prefix) {
    return prefix + '_' + Math.random().toString(36).slice(2);
  },
});

// Static Methods

/**
 * Function used to set the attributes on an element.
 * and unbind events.
 * @param {object} attributes - Hash of attributes to set on base element.
 * @returns {Function} Extended child constructor function.
 */
function extend(attributes) {
  /**
   * Function used as constructor in order to establish inheritance chain.
   * @returns {AtomicComponent} An instance.
   */
  function child() {
    this._super = AtomicComponent.prototype;
    return AtomicComponent.apply(this, arguments);
  }

  child.prototype = Object.create(AtomicComponent.prototype);
  Object.assign(child.prototype, attributes);
  Object.assign(child, AtomicComponent);

  if (
    {}.hasOwnProperty.call(attributes, 'ui') &&
    {}.hasOwnProperty.call(attributes.ui, 'base')
  ) {
    child.selector = attributes.ui.base;
  }

  child.constants = {};

  return child;
}

/**
 * Function used to instantiate all instances of the particular
 * atomic component on a page.
 * @param {HTMLElement} scope - Where to search for components within.
 * @returns {Array} List of AtomicComponent instances.
 */
function init(scope) {
  const components = instantiateAll(this.selector, this, scope);
  return components;
}

// Set public static methods.
AtomicComponent.init = init;
AtomicComponent.extend = extend;

export default AtomicComponent;
