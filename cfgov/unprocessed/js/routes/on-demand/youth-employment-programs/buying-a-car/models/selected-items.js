const defaultProps = {
  maxElements: 3,
  minElements: 1,
};

/**
 * Data structure to manipulate a list of `maxElements` elements.
 * @param {object} props - The properties that configure this data structure.
 * @param {number} props.maxElements - The maximum number of elements
 *   the data structure can hold.
 * @param {number} props.minElements - The minimum number of elements
 *   the data structure should have.
 * @returns {object} The public methods of this data structure.
 */
function selectedItems(props) {
  const finalProps = { ...defaultProps, ...props };
  let items = [];

  /**
   * @returns {boolean} True if max items are selected, false otherwise.
   */
  function isMaxItemsSelected() {
    return items.length === finalProps.maxElements;
  }

  /**
   * @returns {boolean} True if min items are selected, false otherwise.
   */
  function isMinItemsSelected() {
    return items.length >= finalProps.minElements;
  }

  /**
   * TODO: Add jsdocs.
   * @param item
   */
  function add(item) {
    if (!isMaxItemsSelected()) {
      items.push(item);
    }
  }

  /**
   * TODO: Add jsdocs.
   * @param item
   */
  function remove(item) {
    const copy = items.slice();

    copy.splice(items.indexOf(item), 1);

    items = copy;
  }

  /**
   * @returns {number} The number of items.
   */
  function length() {
    return items.length;
  }

  /**
   * @returns {Array} Get all items.
   */
  function elements() {
    return items;
  }

  /**
   * TODO: Add jsdocs.
   */
  function getHead() {
    return items[0];
  }

  /**
   * TODO: Add jsdocs.
   */
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
    remove,
  };
}

export default selectedItems;
