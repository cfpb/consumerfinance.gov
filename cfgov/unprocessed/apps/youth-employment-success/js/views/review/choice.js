import { checkDom, setInitFlag } from '../../../../../js/modules/util/atomic-helpers';
import { toArray } from '../../util';
import { updateRouteChoiceAction } from '../../reducers/choice-reducer';
import inputView from '../input';

const CLASSES = Object.freeze( {
  CONTAINER: 'js-yes-review-choice',
  REVIEW_PLAN: 'js-yes-plans-review',
  BUTTON: 'js-yes-choice-finalize',
  CHOICE_WAIT: 'js-route-selection-wait',
  CHOICE_CLONE: 'js-yes-route-selection-clone'
} );

/**
 * ReviewChoiceView
 *
 * @class
 *
 * @classdesc View to manage form controls that allow user to select their
 * preferred route option and review their final plan
 *
 * @param {HTMLElement} element The container node for this view
 * @param {Object} props The additional properties supplied to this view
 * @param {YesStore} props.store The public API exposed by the Store class
 * @returns {Object} This view's public API
 */
function reviewChoiceView( element, { store, choiceButtonView, onShowReviewPlan } ) {
  const _dom = checkDom( element, CLASSES.CONTAINER );
  const _reviewPlanEl = _dom.querySelector( `.${ CLASSES.REVIEW_PLAN }` );
  // Although three choice buttons are initially shown to handle the case where a user
  // visiting the site without JS enabled elects to print the tool, we only want to
  // initialize one choice button to start
  const _choiceBtnEls = toArray(
    _dom.querySelectorAll( `.${ choiceButtonView.CLASSES.CONTAINER }` )
  );
  const _waitBtnEl = _dom.querySelector( `.${CLASSES.CHOICE_WAIT }` );
  const _reviewBtnEl = _dom.querySelector( `.${ CLASSES.BUTTON }` );

  let _choiceButtonViews = [];
  let _waitButtonView;

  /**
   * Enables the button that displays the final review plan on click
   */
  function _enableReviewButton() {
    _reviewBtnEl.removeAttribute( 'disabled' );
  }

  /**
   * Disabled the button responsible for displaying the final review plan
   */
  function _disableReviewButton() {
    _reviewBtnEl.setAttribute( 'disabled', 'disabled' );
  }

  /**
   * Show the plan review section of the HTML. Remove the event listener since
   * the user won't need to interact with the button again.
   */
  function _showReviewPlan() {
    _reviewPlanEl.classList.remove( 'u-hidden' );
    onShowReviewPlan();
    _reviewBtnEl.removeEventListener( 'click', _showReviewPlan );
  }

  /**
   * Called on page load to hide the review plan
   */
  function _hideReviewPlan() {
    _reviewPlanEl.classList.add( 'u-hidden' );
  }

  /**
   * Update the app's state with the user's first choice of transportation
   * @param {Object} updateObject Object with event information supplied by the InputView component.
   * Used to update app state
   * @param {Object} updateObject.event The DOM event emitted by the input node
   */
  function _handlePlanSelection( { event } ) {
    store.dispatch(
      updateRouteChoiceAction( event.target.value )
    );
  }

  /**
   * Initialize the form controls this view manages
   */
  function _initInputs() { 
    _choiceButtonViews = _choiceBtnEls.map((el, index) => {
      const view = choiceButtonView(el, {
        handleClick: _handlePlanSelection,
        position: index + 1
      });

      view.init();

      return view;
    });

    _waitButtonView = inputView(_waitBtnEl, {
      events: {
        'click': _handlePlanSelection
      },
      type: 'radio'
    });

    // probably need to disable this
    _waitButtonView.init();

    _reviewBtnEl.addEventListener( 'click', _showReviewPlan );
  }

  /**
   * Update HTML this view manages based on the current application state.
   * @param {Object} _ The previous application state object, unused here
   * @param {Object} state The current state of the application
   */
  function _handleStateUpdate( prevState, state ) {
    // TODO: Add selector for all routes
    const prevRoutes = prevState.routes.routes;
    const routes = state.routes.routes;

    // Choice buttons clearly need to be their own view
    if (prevRoutes.length && prevRoutes.length !== routes.length) {
      let nextChoice;
      if (_choiceBtnEls.length === routes.length) {
        /** 
         * The user added the second route. Since the form element starts on the page
         * (to accomodate a user printing the tool), we grab that element and initialize
         * a new choiceView with it. All routes after the second require that we clone
         * a dummy choice form control and populate it.
        **/
        nextChoice = _choiceBtnEls[_choiceBtnEls.length - 1];
      } else {
        nextChoice = _dom.querySelector(`.${CLASSES.CHOICE_CLONE}`)
          .children[0]
          .cloneNode(true);
        _dom.querySelector('.js-route-choices').appendChild(nextChoice);
        nextChoice.classList.add('u-mt15', 'u-mb15');
      }

      const buttonView = choiceButtonView(nextChoice, {
        handleClick: _handlePlanSelection,
        position: _choiceButtonViews.length + 1
      });

      buttonView.init();

      if (_choiceBtnEls.length !== routes.length) {
        _choiceButtonViews.push(buttonView);
      }
    }

    _choiceButtonViews.forEach( (view, i) => {
      view.render({ route: routes[i] });
    });

    // TODO: add selector for this, expand reducer to handle whether or not button was clicked
    if ( state.routeChoice ) {
      _enableReviewButton();
    } else {
      _disableReviewButton();
    }
  }

  return {
    init() {
      if ( setInitFlag( _dom ) ) {
        _hideReviewPlan();
        _initInputs();
        store.subscribe( _handleStateUpdate );
      }
    }
  };
}

reviewChoiceView.CLASSES = CLASSES;

export default reviewChoiceView;
