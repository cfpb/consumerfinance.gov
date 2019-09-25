import { checkDom, setInitFlag } from '../../../../../js/modules/util/atomic-helpers';
import { routeSelector, todoListSelector } from '../../reducers/route-option-reducer';
import { toArray, toggleCFNotification } from '../../util';
import { getPlanItem } from '../../data/todo-items';

const CLASSES = Object.freeze( {
  CONTAINER: 'js-option-review',
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
  const _detailsViews = [];

  /**
   * Event handler to update child views with current state
   * @param {Object} _ The previous state value from store (unused)
   * @param {Object} state The current application state
   */
  function _handleStateUpdate( _, state ) {
    _detailsViews.forEach( ( view, index ) => {
      const currentRoute = routeSelector(
        state.routes,
        index
      );

      if ( Object.keys( currentRoute ).length ) {
        view.render( {
          budget: state.budget,
          route: currentRoute
        } );
      }
    } );

    _todoEls.forEach( ( el, index ) => {
      const fragment = document.createDocumentFragment();
      todoListSelector( state.routes, index ).forEach( todo => {
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
