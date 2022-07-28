function checklistMap( data ) {
  const lookup = data;

  function checklist() {
    return { ...lookup };
  }

  function filterKeysBy( predicate ) {
    const keys = Object.keys( lookup );

    return keys.filter( predicate );
  }

  function get( key ) {
    return lookup[key];
  }

  return {
    checklist,
    get,
    filterKeysBy
  };
}

export default checklistMap;
