import { assign } from '../../../../../../apps/youth-employment-success/js/util';

const defaultProps = {
  maxElements: 3,
  minElements: 1
};

/**
 * Data structure to manipulate a list of `maxElements` elements
 * @param {Object} props The properties that configure this data structure
 * @param {Number} maxElements The maximum number of elements the data structure can hold
 * @param {Number} minElements The minimum number of elements the data structure should have
 * @returns {Object} The public methods of this data structure
 */
function selectedItems( props ) {
  const finalProps = assign( {}, defaultProps, props );
  let items = [];

  function isMaxItemsSelected() {
    return items.length === finalProps.maxElements;
  }

  function isMinItemsSelected() {
    return items.length >= finalProps.minElements;
  }

  function add( item ) {
    if ( !isMaxItemsSelected() ) {
      items.push( item );
    }
  }

  function remove( item ) {
    const copy = items.slice();

    copy.splice( items.indexOf( item ), 1 );

    items = copy;
  }

  function length() {
    return items.length;
  }

  function elements() {
    return items;
  }

  function getHead() {
    return items[0];
  }

  function getLast() {
    return items[items.length - 1];
  }

  return {
    add,
    elements,
    getHead,
    getLast,
    isMaxItemsSelected,
    isMinItemsSelected,
    length,
    remove
  };
}

export default selectedItems;
