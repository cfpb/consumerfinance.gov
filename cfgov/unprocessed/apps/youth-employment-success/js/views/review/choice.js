import { checkDom, setInitFlag } from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';
import { toArray } from '../../util';
import { updateRouteChoiceAction } from '../../reducers/choice-reducer';
import inputView from '../input';
import transportationMap from '../../data-types/transportation-map';

const CLASSES = Object.freeze( {
  CONTAINER: 'js-yes-review-choice',
  REVIEW_PLAN: 'js-yes-plans-review',
  BUTTON: 'js-yes-choice-finalize',
  CHOICE: 'js-yes-route-selection'
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
function reviewChoiceView( element, { store, onShowReviewPlan } ) {
  const _dom = checkDom( element, CLASSES.CONTAINER );
  const _reviewPlanEl = _dom.querySelector( `.${ CLASSES.REVIEW_PLAN }` );
  const _choiceBtnEls = toArray(
    _dom.querySelectorAll( `.${ CLASSES.CHOICE }` )
  );
  const _choiceInputs = _choiceBtnEls.map( el => el.querySelector( 'input' ) );
  const _reviewBtnEl = _dom.querySelector( `.${ CLASSES.BUTTON }` );

  /**
   * Allow user to interact with this view's radio button form elements
   */
  function _enableChoices() {
    _choiceInputs.forEach( el => el.removeAttribute( 'disabled' ) );
  }

  /**
   * Disable route option selection radio button
   */
  function _disableChoices() {
    _choiceInputs.forEach( el => el.setAttribute( 'disabled', 'disabled' )
    );
  }

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
   * Sets the labels of each route selection radio button to the
   * mode of transportation the user indicated.
   * @param {Object} routes An array of route option objects
   */
  function _populateOptionLabels( routes ) {
    _choiceBtnEls.forEach( ( el, index ) => {
      const route = routes[index];

      // Need a check here because the third option isnt tied to a route
      if ( route ) {
        const label = el.querySelector( 'label' );
        const friendlyOption = transportationMap[route.transportation];
        const nextLabel = `Option ${ index + 1 }: ${ friendlyOption }`;
        label.textContent = nextLabel;
      }
    } );
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
    _choiceInputs.forEach( el => {
      inputView( el, {
        events: {
          click: _handlePlanSelection
        },
        type: 'radio'
      } ).init();
    } );

    _reviewBtnEl.addEventListener( 'click', _showReviewPlan );
  }

  /**
   * Determines if a given route has a transportation type indicated
   * @param {Object} route A route object
   * @returns {Boolean} If the route has a specified mode of transportation
   */
  function _routeHasTransportation( route ) {
    return route && Boolean( route.transportation );
  }

  /**
   * Update HTML this view manages based on the current application state.
   * @param {Object} _ The previous application state object, unused here
   * @param {Object} state The current state of the application
   */
  function _handleStateUpdate( _, state ) {
    const routes = state.routes.routes;
    let transportationSelected = true;

    for ( let i = 0; i < routes.length; i++ ) {
      const route = routes[i];

      if ( !_routeHasTransportation( route ) ) {
        transportationSelected = false;
      }
    }

    if ( transportationSelected ) {
      _enableChoices();
      _populateOptionLabels( routes );
    }

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

        /**
         * NOTE: Although these are set to disabled in the template, we need to manually disable them again;
         * all form controls are enabled once JS is detected. These fields are a special
         * case in that they are the only form controls which are conditionally available,
         * based on valid data being input by the user.
        */
        _disableChoices();
        _initInputs();
        store.subscribe( _handleStateUpdate );
      }
    }
  };
}

reviewChoiceView.CLASSES = CLASSES;

export default reviewChoiceView;
