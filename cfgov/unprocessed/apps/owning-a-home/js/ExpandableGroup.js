// Required modules.
import { checkDom, setInitFlag }
  from '../../../js/modules/util/atomic-helpers';
import Expandable from './Expandable';
import standardType from '../../../js/modules/util/standard-type';

/**
 * ExpandableGroup
 * @class
 *
 * @classdesc Initializes a new Expandable Group organism.
 *
 * @param {HTMLNode} element Base element.
 * @param {object} options Customization options.
 *   The DOM element within which to search for the organism.
 * @returns {Object} An ExpandableGroup instance.
 */
function ExpandableGroup( element, options = {} ) {

  const BASE_CLASS = 'o-expandable-group';
  const _dom = checkDom( element, BASE_CLASS );
  const _domChildren = _dom.querySelectorAll( '.o-expandable' );
  let _lastOpenChild;
  let _isAccordion;

  this.options = options;
  this.collapseDuration = options.collapseDuration;

  /**
   * @returns {ExpandableGroup|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init() {
    if ( !setInitFlag( _dom ) ) {
      return standardType.UNDEFINED;
    }

    _isAccordion = _dom.classList.contains( BASE_CLASS + '__accordion' );

    let child;
    const len = _domChildren.length;

    for ( let i = 0; i < len; i++ ) {
      child = new Expandable( _domChildren[i] ).init();
      child.addEventListener( 'expandBegin', _childBeginExpand.bind( this ) );
    }

    return this;
  }

  /**
   * Handle opening event of a child Expandable instance.
   * @param {Object} ev An object that references the event target.
   */
  function _childBeginExpand( ev ) {
    if ( _isAccordion ) {
      if ( _lastOpenChild && _lastOpenChild !== ev.target ) {
        _lastOpenChild.collapse( this.collapseDuration );
      }
      _lastOpenChild = ev.target;
    }
  }

  this.init = init;
  return this;
}

export default ExpandableGroup;
