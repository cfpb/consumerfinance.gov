import { checkDom, setInitFlag } from '../../../js/modules/util/atomic-helpers';

const CLASSES = Object.freeze( {
  BUTTON: 'm-yes-route-option'
} );

function routeOptionToggleView( element, { expandable, routeOptionForm } ) {
  const _dom = checkDom( element, CLASSES.BUTTON );

  function _showRouteOption() {
    expandable.element.querySelector( '.o-expandable_target' ).click();
    expandable.element.classList.remove( 'u-hidden' );
    _dom.classList.add( 'u-hidden' );
    _dom.removeEventListener( 'click', _showRouteOption );
    routeOptionForm.init();
  }

  return {
    init() {
      if ( setInitFlag( _dom ) ) {
        _dom.addEventListener( 'click', _showRouteOption );
      }
    }
  };
}

routeOptionToggleView.CLASSES = CLASSES;

export default routeOptionToggleView;
