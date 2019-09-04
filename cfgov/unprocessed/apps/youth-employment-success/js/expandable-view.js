import { checkDom, setInitFlag } from '../../../js/modules/util/atomic-helpers';

const CLASSES = Object.freeze({
  CONTAINER: 'o-expandable'
});

function expandableView(element, { expandable }) {
  const _dom = checkDom(element, CLASSES.CONTAINER);
  let initialized = false;

  if (!expandable) {
    throw new Error('An instance of an expandable is a required prop.');
  }

  function _hideRouteDetails() {
    
  }

  function _showRouteDetails() {  
    _dom.appendChild(_dom.querySelector('.yes-route-details').cloneNode(true));
  }

  return {
    init() {
      if (!initialized) {
        expandable.transition.addEventListener('expandBegin', _hideRouteDetails);
        expandable.transition.addEventListener('collapseEnd', _showRouteDetails);
        initialized = true;
      }
    }
  }
}

export default expandableView;
