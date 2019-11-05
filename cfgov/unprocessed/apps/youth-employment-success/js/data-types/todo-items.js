const PLAN_TYPES = Object.freeze( {
  AVERAGE_COST: 'AVERAGE_COST',
  DAYS_PER_WEEK: 'DAYS_PER_WEEK',
  MILES: 'MILES',
  TIME: 'TIME'
} );

const ACTION_PLAN = Object.freeze( {
  AVERAGE_COST: 'Look up average daily cost.',
  DAYS_PER_WEEK: 'Find out how many days per week you\'ll make this trip.',
  MILES: ' Look up how many miles you drive each day.',
  TIME: ' Look up how long this trip takes.'
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
