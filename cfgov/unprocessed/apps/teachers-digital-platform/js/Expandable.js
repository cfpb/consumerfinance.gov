// TODO: Note that this is an older copy of Expandable from the
// design-system to isolate TDP expandable customizations.

/* ==========================================================================
   Expandable Organism
   ========================================================================== */

import AtomicComponent from './AtomicComponent.js';
import { EventObserver } from '@cfpb/cfpb-design-system';
import ExpandableTransition from './ExpandableTransition.js';

const eventObserver = new EventObserver();

/**
 * Event handler for when an expandable begins expanding.
 */
function expandBeginHandler() {
  this.ui.content.classList.remove('u-hidden');
}

/**
 * Event handler for when an expandable is finished collapsing.
 */
function collapseEndHandler() {
  this.ui.content.classList.add('u-hidden');
}

/**
 * Event handler for when an accordion is activated
 */
function _accordionActivatedHandler() {
  if (this.activeAccordion) {
    this.transition.toggleExpandable();
    this.toggleTargetState(this.ui.target);
    this.activeAccordion = false;
  }
}

/**
 * Initialize a new expandable.
 */
function initialize() {
  const transition = new ExpandableTransition(this.ui.content);
  this.transition = transition.init();
  this.transition.addEventListener(
    'expandBegin',
    expandBeginHandler.bind(this),
  );
  this.transition.addEventListener(
    'collapseEnd',
    collapseEndHandler.bind(this),
  );

  if (
    this.ui.content.classList.contains(ExpandableTransition.CLASSES.EXPANDED)
  ) {
    this.ui.target.classList.add(this.classes.targetExpanded);
  } else {
    this.ui.target.classList.add(this.classes.targetCollapsed);
    this.ui.content.classList.add('u-hidden');
  }

  const expandableGroup = this.ui.target.closest('.' + this.classes.group);

  this.isAccordionGroup =
    expandableGroup !== null &&
    expandableGroup.classList.contains(this.classes.groupAccordion);

  if (this.isAccordionGroup) {
    eventObserver.addEventListener(
      'accordionActivated',
      _accordionActivatedHandler.bind(this),
    );
  }
}

/**
 * Event handler for when an expandable is clicked.
 */
function expandableClickHandler() {
  this.transition.toggleExpandable();
  this.toggleTargetState(this.ui.target);

  if (this.isAccordionGroup) {
    if (this.activeAccordion) {
      this.activeAccordion = false;
    } else {
      eventObserver.dispatchEvent('accordionActivated', { target: this });
      this.activeAccordion = true;
    }
  }
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

/**
 * Retrieve the label text of the expandable header.
 * @returns {string} The text of the expandable's label.
 */
function getLabelText() {
  return this.ui.label.textContent.trim();
}

const Expandable = AtomicComponent.extend({
  ui: {
    base: '.o-expandable',
    target: '.o-expandable__header',
    content: '.o-expandable__content',
    header: '.o-expandable__header',
    label: '.o-expandable__label',
  },

  classes: {
    targetExpanded: 'o-expandable__target--expanded',
    targetCollapsed: 'o-expandable__target--collapsed',
    group: 'o-expandable-group',
    groupAccordion: 'o-expandable-group--accordion',
  },

  events: {
    'click .o-expandable__header': 'expandableClickHandler',
  },

  transition: null,
  isAccordionGroup: false,
  activeAccordion: false,

  initialize: initialize,
  expandableClickHandler: expandableClickHandler,
  toggleTargetState: toggleTargetState,
  getLabelText: getLabelText,
});

export default Expandable;
