/* ==========================================================================
   Expandable Facets Organism
   ========================================================================== */

// polyfill for ie9 compatibility
require( 'classlist-polyfill' );

import { closest } from '@cfpb/cfpb-atomic-component/src/utilities/dom-traverse.js';

import EventObserver from '@cfpb/cfpb-atomic-component/src/mixins/EventObserver.js';
import AtomicComponent from '@cfpb/cfpb-atomic-component/src/components/AtomicComponent.js';
const ExpandableFacetTransition = require( './ExpandableFacetTransition' );

const ExpandableFacets = AtomicComponent.extend( {
  ui: {
    base:           '.o-expandable-facets',
    target:         '.o-expandable-facets_target',
    content:        '.o-expandable-facets_content',
    header:         '.o-expandable_header',
    facetCheckbox:  '.o-expandable-facets_checkbox',
    facetLabel:     '.o-expandable-facets_checkbox ~ .a-label'
  },

  classes: {
    targetExpanded:  'is-open',
    targetCollapsed: 'is-closed',
    group:           'o-expandable-group',
    groupAccordion:  'o-expandable-group__accordion'
  },

  events: {
    'click .o-expandable-facets_target': 'expandableClickHandler'
  },

  transition:       null,
  isAccordionGroup: false,
  activeAccordion:  false,

  initialize:             initialize,
  expandableClickHandler: expandableClickHandler,
  toggleTargetState:      toggleTargetState
} );

/**
 * Initialize a new expandable.
 */
function initialize() {
  const customClasses = {
    BASE_CLASS:   'o-expandable-facets_content__transition',
    EXPANDED:     'o-expandable-facets_content__expanded',
    COLLAPSED:    'o-expandable-facets_content__collapsed',
    OPEN_DEFAULT: 'o-expandable-facets_content__onload-open'
  };

  const transition = new ExpandableFacetTransition(
    this.ui.content, customClasses
  );
  this.transition = transition.init();

  if ( this.ui.content.classList.contains( customClasses.OPEN_DEFAULT ) ) {
    this.ui.target.classList.add( this.classes.targetExpanded );
  } else {
    this.ui.target.classList.add( this.classes.targetCollapsed );
  }

  const expandableGroup = closest(
    this.ui.target, '.' + this.classes.group
  );

  this.isAccordionGroup = expandableGroup !== null &&
    expandableGroup.classList.contains( this.classes.groupAccordion );

  if ( this.isAccordionGroup ) {
    EventObserver.addEventListener(
      'accordionActivated',
      _accordionActivatedHandler.bind( this )
    );
  }

  if ( this.ui.facetCheckbox.hasAttribute( 'checked' ) ||
    this.ui.facetLabel.classList.contains( 'indeterminate' ) ) {
    this.transition.toggleExpandable();
    this.toggleTargetState( this.ui.target );
  }
}

/**
 * Event handler for when an accordion is activated
 */
function _accordionActivatedHandler() {
  if ( this.activeAccordion ) {
    this.transition.toggleExpandable();
    this.toggleTargetState( this.ui.target );
    this.activeAccordion = false;
  }
}

/**
 * Event handler for when an expandable is clicked.
 */
function expandableClickHandler() {
  this.transition.toggleExpandable();
  this.toggleTargetState( this.ui.target );

  if ( this.isAccordionGroup ) {
    if ( this.activeAccordion ) {
      this.activeAccordion = false;
    } else {
      EventObserver.dispatchEvent( 'accordionActivated', { target: this } );
      this.activeAccordion = true;
    }
  }
}

/**
 * Toggle an expandable to open or closed.
 * @param {HTMLNode} element - The expandable target HTML DOM element.
 */
function toggleTargetState( element ) {
  if ( element.classList.contains( this.classes.targetExpanded ) ) {
    this.ui.target.classList.add( this.classes.targetCollapsed );
    this.ui.target.classList.remove( this.classes.targetExpanded );
  } else {
    this.ui.target.classList.add( this.classes.targetExpanded );
    this.ui.target.classList.remove( this.classes.targetCollapsed );
  }
}

module.exports = ExpandableFacets;

/**
 * Find .o-expandable-facets, add `is-open` class.
 * Find .o-expandable-facets_target and add a click handler to toggle classes on .o-expandable-facets between `is-open` and `is-closed`.
 */
