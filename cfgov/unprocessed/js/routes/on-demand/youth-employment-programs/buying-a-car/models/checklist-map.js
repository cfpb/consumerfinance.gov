/**
 *
 * @param data
 */
function checklistMap(data) {
  const lookup = data;

  /**
   *
   */
  function checklist() {
    return { ...lookup };
  }

  /**
   *
   * @param predicate
   */
  function filterKeysBy(predicate) {
    const keys = Object.keys(lookup);

    return keys.filter(predicate);
  }

  /**
   *
   * @param key
   */
  function get(key) {
    return lookup[key];
  }

  return {
    checklist,
    get,
    filterKeysBy,
  };
}

export default checklistMap;
