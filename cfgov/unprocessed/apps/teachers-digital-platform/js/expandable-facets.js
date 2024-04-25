/* ==========================================================================
   Expandable Facets Organism
   ========================================================================== */

import AtomicComponent from './AtomicComponent.js';
import ExpandableFacetTransition from './ExpandableFacetTransition.js';

const ExpandableFacets = AtomicComponent.extend({
  ui: {
    base: '.o-expandable-facets',
    target: '.o-expandable-facets__target',
    content: '.o-expandable-facets__content',
    header: '.o-expandable__header',
    facetCheckbox: '.o-expandable-facets__checkbox',
    facetLabel: '.o-expandable-facets__checkbox ~ .a-label',
  },

  classes: {
    targetExpanded: 'is-open',
    targetCollapsed: 'is-closed',
    group: 'o-expandable-group',
  },

  events: {
    'click .o-expandable-facets__target': 'expandableClickHandler',
  },

  transition: null,

  initialize: initialize,
  expandableClickHandler: expandableClickHandler,
  toggleTargetState: toggleTargetState,
});

/**
 * Initialize a new expandable.
 */
function initialize() {
  const customClasses = {
    BASE_CLASS: 'o-expandable-facets__content--transition',
    EXPANDED: 'o-expandable-facets__content--expanded',
    COLLAPSED: 'o-expandable-facets__content--collapsed',
    OPEN_DEFAULT: 'o-expandable-facets__content--onload-open',
  };

  const transition = new ExpandableFacetTransition(
    this.ui.content,
    customClasses,
  );
  this.transition = transition.init(
    ExpandableFacetTransition.CLASSES.COLLAPSED,
  );

  if (this.ui.content.classList.contains(customClasses.OPEN_DEFAULT)) {
    this.ui.target.classList.add(this.classes.targetExpanded);
  } else {
    this.ui.target.classList.add(this.classes.targetCollapsed);
  }

  if (
    this.ui.facetCheckbox.hasAttribute('checked') ||
    this.ui.facetLabel.classList.contains('indeterminate')
  ) {
    this.transition.toggleExpandable();
    this.toggleTargetState(this.ui.target);
  }
}

/**
 * Event handler for when an expandable is clicked.
 */
function expandableClickHandler() {
  this.transition.toggleExpandable();
  this.toggleTargetState(this.ui.target);
}

/**
 * Toggle an expandable to open or closed.
 * @param {HTMLElement} element - The expandable target HTML DOM element.
 */
function toggleTargetState(element) {
  if (element.classList.contains(this.classes.targetExpanded)) {
    this.ui.target.classList.add(this.classes.targetCollapsed);
    this.ui.target.classList.remove(this.classes.targetExpanded);
  } else {
    this.ui.target.classList.add(this.classes.targetExpanded);
    this.ui.target.classList.remove(this.classes.targetCollapsed);
  }
}

export default ExpandableFacets;

/**
 * Find .o-expandable-facets, add `is-open` class.
 * Find .o-expandable-facets__target and add a click handler to toggle classes on .o-expandable-facets between `is-open` and `is-closed`.
 */
