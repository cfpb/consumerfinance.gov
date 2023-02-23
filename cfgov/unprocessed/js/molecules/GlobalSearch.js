import { DESKTOP, viewportIsIn } from '../modules/util/breakpoint-state.js';
import {
  checkDom,
  setInitFlag,
} from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';
import ClearableInput from '../modules/ClearableInput.js';
import EventObserver from '@cfpb/cfpb-atomic-component/src/mixins/EventObserver.js';
import FlyoutMenu from '@cfpb/cfpb-atomic-component/src/utilities/behavior/FlyoutMenu.js';
import MoveTransition from '@cfpb/cfpb-atomic-component/src/utilities/transition/MoveTransition.js';
import TabTrigger from '../modules/TabTrigger.js';

const BASE_CLASS = 'm-global-search';

/**
 * GlobalSearch
 *
 * @class
 * @classdesc Initializes a new GlobalSearch molecule.
 * @param {HTMLElement} element - The DOM element within which to search
 *   for the molecule.
 * @returns {GlobalSearch} An instance.
 */
function GlobalSearch(element) {
  const _dom = checkDom(element, BASE_CLASS);
  const _contentDom = _dom.querySelector(`.${BASE_CLASS}_content`);
  const _triggerDom = _dom.querySelector(`.${BASE_CLASS}_trigger`);
  const _triggerCloseLabelText = _triggerDom
    .querySelector(`.${BASE_CLASS}_trigger-close-label`)
    .innerText.trim();
  const _triggerOpenLabelText = _triggerDom
    .querySelector(`.${BASE_CLASS}_trigger-open-label`)
    .innerText.trim();
  const _flyout = new FlyoutMenu(_dom);
  let _searchInputDom;
  let _searchBtnDom;
  let _clearBtnDom;

  /* The tab trigger adds an element to the end of the element that handles
     cleanup after tabbing out of the element. */
  const _tabTrigger = new TabTrigger(_dom);

  /**
   * @returns {GlobalSearch} An instance.
   */
  function init() {
    if (!setInitFlag(_dom)) {
      return this;
    }

    // Set initial appearance.
    const transition = new MoveTransition(_contentDom).init(
      MoveTransition.CLASSES.MOVE_RIGHT
    );
    _flyout.setTransition(
      transition,
      transition.moveRight,
      transition.moveToOrigin
    );
    _flyout.init();

    _contentDom.classList.remove('u-hidden');

    const clearBtnSel = `.${BASE_CLASS} .input-contains-label_after__clear`;
    const inputContainsLabelSel = `.${BASE_CLASS}_content-form .input-contains-label`;
    const searchBtnSel = `.${BASE_CLASS} .o-form__input-w-btn_btn-container button`;

    _clearBtnDom = _contentDom.querySelector(clearBtnSel);
    const inputContainsLabel = _contentDom.querySelector(inputContainsLabelSel);
    _searchInputDom = inputContainsLabel.querySelector('input');
    _searchBtnDom = _contentDom.querySelector(searchBtnSel);

    // Initialize new clearable input behavior on the input-contains-label.
    const clearableInput = new ClearableInput(inputContainsLabel);
    clearableInput.init();
    const handleExpandBeginBinded = _handleExpandBegin.bind(this);
    const handleCollapseEndBinded = _handleCollapseEnd.bind(this);

    _flyout.addEventListener('expandbegin', handleExpandBeginBinded);
    _flyout.addEventListener('expandend', () => {
      _searchInputDom.select();
    });
    _flyout.addEventListener('collapsebegin', _handleCollapseBegin);
    _flyout.addEventListener('collapseend', handleCollapseEndBinded);

    _tabTrigger.init();
    _tabTrigger.addEventListener('tabpressed', () => {
      if (_flyout.isExpanded()) {
        collapse();
      }
    });

    // Set initial collapse state.
    _contentDom.classList.add('u-invisible');

    return this;
  }

  /**
   * Event handler for when there's a click on the page's body.
   * Used to close the global search, if needed.
   *
   * @param {MouseEvent} event - The event object for the mousedown event.
   */
  function _handleBodyClick(event) {
    const target = event.target;

    const isInDesktop = viewportIsIn(DESKTOP);
    if (
      (isInDesktop && !_isDesktopTarget(target)) ||
      (!isInDesktop && !_isMobileTarget(target))
    ) {
      collapse();
    }
  }

  /**
   * Whether a target is one of the ones that appear in the desktop view.
   *
   * @param {HTMLElement} target - The target of a mouse event (most likely).
   * @returns {boolean} True if the passed target is in the desktop view.
   */
  function _isDesktopTarget(target) {
    return (
      target === _searchInputDom ||
      target === _searchBtnDom ||
      target === _clearBtnDom
    );
  }

  /**
   * Whether a target is one of the ones that appear in the mobile view.
   *
   * @param {HTMLElement} target - The target of a mouse event (most likely).
   * @returns {boolean} True if the passed target is in the mobile view.
   */
  function _isMobileTarget(target) {
    return _dom.contains(target);
  }

  /**
   * Event handler for when FlyoutMenu expand transition begins.
   * Use this to perform post-expandbegin actions.
   */
  function _handleExpandBegin() {
    this.dispatchEvent('expandbegin', { target: this });

    /* TODO: Remove when Android 4.0-4.4 support is dropped.
       Hack to fix reflow issues on legacy Android devices. */
    /*_contentDom.style.display = 'none';
    // eslint-disable-next-line no-unused-expressions
    _contentDom.offsetHeight;
    _contentDom.style.display = '';
    */
    _contentDom.classList.remove('u-invisible');

    //_searchInputDom.select();

    _triggerDom.setAttribute('aria-label', _triggerCloseLabelText);

    document.body.addEventListener('mousedown', _handleBodyClick);
  }

  /**
   * Event handler for when FlyoutMenu collapse transition begins.
   * Use this to perform post-collapsebegin actions.
   */
  function _handleCollapseBegin() {
    _searchInputDom.blur();
    _triggerDom.setAttribute('aria-label', _triggerOpenLabelText);
    document.body.removeEventListener('mousedown', _handleBodyClick);
  }

  /**
   * Event handler for when FlyoutMenu collapse transition ends.
   * Use this to perform post-collapseend actions.
   */
  function _handleCollapseEnd() {
    this.dispatchEvent('collapseend', { target: this });

    /* TODO: When tabbing is used to collapse the search flyout
       it will not animate with the below line.
       Investigate why this is the case for tab key
       but not with mouse clicks. */
    _contentDom.classList.add('u-invisible');
  }

  /**
   * Close the search box.
   *
   * @returns {object} An GlobalSearch instance.
   */
  function collapse() {
    _flyout.collapse();

    return this;
  }

  // Attach public events.
  const eventObserver = new EventObserver();
  this.addEventListener = eventObserver.addEventListener;
  this.removeEventListener = eventObserver.removeEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;

  this.init = init;
  this.collapse = collapse;

  return this;
}

export default GlobalSearch;
