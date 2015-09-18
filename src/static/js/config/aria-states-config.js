/* ==========================================================================
   Aria State

   Code copied from the following with minor modifications:

   - https://github.com/IBM-Watson/a11y.js
     Copyright (c) 2014 IBM

   - http://www.w3.org/TR/wai-aria/states_and_properties
   ========================================================================== */
'use strict';

var UNDEFINED;

var states = {
  // Indicates whether an element, and its subtree,
  // are currently being updated.
  'aria-busy': {
    validElements: [ 'all' ],
    validValues:   [ true, false ]
  },

  // Indicates the current "checked" state of checkboxes, radio buttons,
  // and other widgets. See related aria-pressed and aria-selected.
  'aria-checked': {
    validElements: [ 'all' ],
    validValues:   [ true, false, 'mixed', UNDEFINED ]
  },

  // Indicates that the element is perceivable but disabled, so it is
  // not editable or otherwise operable. See related aria-hidden
  // and aria-readonly.
  'aria-disabled': {
    validElements: [ 'all' ],
    validValues:   [ true, false, 'mixed', UNDEFINED ]
  },

  // Indicates whether the element, or another grouping element
  // it controls, is currently expanded or collapsed.
  'aria-expanded': {
    validElements: [ 'button', 'document', 'link', 'section', 'sectionhead',
      'separator', 'window' ],
    validValues: [ true, false, UNDEFINED ]
  },
  // Indicates an element's "grabbed" state in a drag-and-drop operation.
  'aria-grabbed': {
    validElements: [ 'all' ],
    validValues:   [ true, false, UNDEFINED ]
  },

  // Indicates that the element and all of its descendants are not visible
  // or perceivable to any user as implemented by the author. See related
  // aria-disabled.
  'aria-hidden': {
    validElements: [ 'all' ],
    validValues:   [ true, false, UNDEFINED ]
  },

  // Indicates the entered value does not conform to the format
  // expected by the application.
  'aria-invalid': {
    validElements: [ 'all' ],
    validValues:   [ true, false, 'grammar', 'spelling' ]
  },

  // Indicates the current "pressed" state of toggle buttons.
  'aria-pressed': {
    validElements: [ 'all' ],
    validValues:   [ true, false, 'mixed', UNDEFINED ]
  },

  // Indicates the current "selected" state of various widgets.
  'aria-selected': {
    validElements: [ 'gridcell', 'option', 'row', 'tab' ],
    validValues:   [ true, false, UNDEFINED ]
  }
};

module.exports = states;
