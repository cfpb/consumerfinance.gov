import { checkDom, setInitFlag } from '../../../../../js/modules/util/atomic-helpers';
import { toArray, toggleCFNotification } from '../../util';
import { getPlanItem } from '../../data/todo-items';
import { isWaiting } from '../../reducers/choice-reducer';
import { todoListSelector } from '../../reducers/route-option-reducer';
import transportationMap from '../../data/transportation-map';

const CLASSES = Object.freeze( {
  CONTAINER: 'js-yes-plans-review',
  CHOICE_HEADING: 'js-review-choice-heading',
  TRANSPORTATION_TYPE: 'js-transportation-option',
  DETAILS: 'yes-route-details',
  TODO: 'js-review-todo',
  ALERT: 'js-route-incomplete'
} );

/**
 * ReviewDetailsView
 *
 * @class
 *
 * @classdesc View to display details of user's route selections in the
 * review section
 *
 * @param {HTMLElement} element The container node for this view
 * @param {Object} props The additional properties supplied to this view
 * @param {YesStore} props.store The public API exposed by the Store class
 * @param {Function} props.routeDetailsView The child view managed by this view,
 * duplicates the information shown in the details section of the route option
 * form
 * @returns {Object} This view's public API
 */
function reviewDetailsView( element, { store, routeDetailsView } ) {
  const _dom = checkDom( element, CLASSES.CONTAINER );
  const _todoEls = toArray(
    _dom.querySelectorAll( `.${ CLASSES.TODO }` )
  );
  const _detailsEls = toArray(
    _dom.querySelectorAll( `.${ CLASSES.DETAILS }` )
  );
  const _notificationEls = toArray(
    _dom.querySelectorAll( `.${ CLASSES.ALERT }` )
  );
  const _transportationTypeEls = toArray(
    _dom.querySelectorAll( `.${ CLASSES.TRANSPORTATION_TYPE }` )
  );
  const _reviewChoiceHeadingEls = toArray(
    _dom.querySelectorAll( `.${ CLASSES.CHOICE_HEADING }` )
  );

  const _detailsViews = [];

  /**
   * Event handler to update child views with current state
   * @param {Object} _ The previous state value from store (unused)
   * @param {Object} state The current application state
   */
  function _handleStateUpdate( _, state ) {
    const otherRoutes = state.routes.routes.slice();
    const preferredRoute = otherRoutes.splice( state.routeChoice, 1 );
    const finalRoutes = preferredRoute.concat( otherRoutes );

    _detailsViews.forEach( ( view, index ) => {
      const route = finalRoutes[index] || {};

      if ( Object.keys( route ).length ) {
        const transporationDesc = transportationMap[route.transportation];
        _transportationTypeEls[index].textContent = transporationDesc;

        view.render( {
          budget: state.budget,
          route
        } );
      }
    } );

    _todoEls.forEach( ( el, index ) => {
      const fragment = document.createDocumentFragment();
      const todos = todoListSelector( state.routes, index );

      if ( todos.length ) {
        el.parentNode.classList.remove( 'u-hidden' );
      } else {
        el.parentNode.classList.add( 'u-hidden' );
      }

      todos.forEach( todo => {
        const item = document.createElement( 'li' );
        item.textContent = getPlanItem( todo );
        fragment.appendChild( item );
      } );

      el.innerHTML = '';
      el.appendChild( fragment );
    } );

    _notificationEls.forEach( ( el, index ) => {
      const todos = todoListSelector( state.routes, index );
      toggleCFNotification( el, todos.length );
    } );

    if ( isWaiting( state ) ) {
      _reviewChoiceHeadingEls.forEach( el => el.classList.add( 'u-hidden' ) );
    } else {
      _reviewChoiceHeadingEls.forEach( el => el.classList.remove( 'u-hidden' ) );
    }
  }

  /**
   * Initialize the child views this view manages.
   */
  function _initSubviews() {
    _detailsEls.reduce( ( memo, node ) => {
      const view = routeDetailsView( node );

      memo.push( view );

      view.init();

      return memo;
    }, _detailsViews );
  }

  return {
    init() {
      if ( setInitFlag( _dom ) ) {
        _initSubviews();
        store.subscribe( _handleStateUpdate );
      }
    }
  };
}

reviewDetailsView.CLASSES = CLASSES;

export default reviewDetailsView;
