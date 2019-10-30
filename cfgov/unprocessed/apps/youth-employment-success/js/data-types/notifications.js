const ALERT_TYPES = Object.freeze( {
  NONE: 'NONE',
  INVALID: 'INVALID',
  IN_BUDGET: 'IN_BUDGET',
  OUT_OF_BUDGET: 'OUT_OF_BUDGET',
  HAS_TODOS: 'HAS_TODOS'
} );

/**
 * Bitmask to resolve which alert should be shown in the
 * `route-details` section, based on the current state of the
 * form.
 *
 * Using a bitmask here has some advantages:
 *
 * 1). It reduces the need for messy if/else logic.
 * 2). It enables new flags to be added easily when alert logic requirements change.
 * 3). It provides basic state-machine / rules engine-like behavior
 *     without needing a lot of code.
 * 4). It ensures that no matter what the state of the application, there will
 *     be at most one displayed alert, and which alert is shown won't need to be resolved
 *     hierarchically.
 * 5). It leaves the final implementation of what alerts should be shown
 *     up to the view making use of the bitmask.
 *
 * The bitmask's values are each a power of two. Left-shifting
 * 1 by an increasing right-hand operand handles this automatically
 * by resolving to the following formula:
 *
 * Where x is the left-hand operand and n is the right:
 *
 * x * (2 ^ n), or e.g. 1 * (2 ^ 3) -> 8.
 *
 */
const ALERT_BITMASK_ENUM = Object.freeze( {
  [ALERT_TYPES.NONE]: 0,
  [ALERT_TYPES.INVALID]: 1,
  [ALERT_TYPES.IN_BUDGET]: 1 << 1,
  [ALERT_TYPES.OUT_OF_BUDGET]: 1 << 2,
  [ALERT_TYPES.HAS_TODOS]: 1 << 3
} );

/**
 * Given a values object, with keys that map to the ALERT_TYPES defined here,
 * resolve the final value of the bitmask.
 * @param {Object} values An object of values that maps to the `ALERT_TYPES` enum.
 * @returns {number} The value of the bitmask.
 */
function getBitmask( values = {} ) {
  let mask = 0;

  for ( const name in values ) {
    if ( values.hasOwnProperty( name ) ) {
      const value = values[name];

      if ( value ) {
        mask |= ALERT_BITMASK_ENUM[name] || ALERT_BITMASK_ENUM.NONE;
      }
    }
  }

  return mask;
}

/**
 * @param {string} type A bitmask flag label.
 * @returns {string} The bitmask flag label.
 */
function getBitValue( type ) {
  return ALERT_BITMASK_ENUM[type] || ALERT_BITMASK_ENUM[ALERT_TYPES.NONE];
}

export {
  ALERT_TYPES,
  ALERT_BITMASK_ENUM,
  getBitValue,
  getBitmask
};
