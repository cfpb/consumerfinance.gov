const PLAN_TYPES = Object.freeze( {
  AVERAGE_COST: 'AVERAGE_COST',
  DAYS_PER_WEEK: 'DAYS_PER_WEEK',
  MILES: 'MILES',
  TIME: 'TIME'
} );

const ACTION_PLAN = Object.freeze( {
  AVERAGE_COST: 'average',
  DAYS_PER_WEEK: 'days per week',
  MILES: 'miles',
  TIME: 'Look up how to estimate transit time.'
} );

/**
 *
 * @param {string} type The name of the item to add to the action plan
 * @returns {String} The text of the action plan item
 */
function getPlanItem( type ) {
  return ACTION_PLAN[type];
}

export {
  PLAN_TYPES,
  getPlanItem
};
