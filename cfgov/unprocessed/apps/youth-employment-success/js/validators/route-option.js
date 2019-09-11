import { PLAN_TYPES } from '../data/todo-items';
import { isNumber } from '../util';

/* Fields that are always required, regardless of the transportation
   mode selected */
const requiredFields = [
  'earned',
  'spent',
  'transportation',
  'transitTimeHours',
  'transitTimeMinutes'
];

const todoListFields = {
  transitTimeHours: PLAN_TYPES.TIME,
  transitTimeMinutes: PLAN_TYPES.TIME,
  milesPerDay: PLAN_TYPES.MILES,
  daysPerWeek: PLAN_TYPES.DAYS_PER_WEEK,
  averageCost: PLAN_TYPES.AVERAGE_COST
};

/**
 * Check if a missing required form field is actually a user selecting
 * 'not sure' as an answer to the form field
 * @param {string} fieldName The name of the field to check
 * @param {array} routeTodoList The current list of items in the user's todo list
 * @returns {Boolean} Data validity
 */
function isFieldInActionPlan( fieldName, routeTodoList ) {
  const todoListValue = todoListFields[fieldName];

  if ( routeTodoList.indexOf( todoListValue ) !== -1 ) {
    return true;
  }

  return false;
}

/**
 * Check if all required fields are present
 * @param {object} data The route option form data
 * @returns {Boolean} Data validity
 */
function isRequiredValid( data ) {
  return requiredFields.reduce( ( memo, fieldName ) => {
    // does the data object contain the required field
    if ( data.hasOwnProperty( fieldName ) ) {
      // check if the value exists
      if (
        !data[fieldName] &&
        !isFieldInActionPlan( fieldName, data.actionPlanItems )
      ) {
        memo = false;
      } else {
        memo = true;
      }
    } else {
      memo = false;
    }

    return memo;
  }, true );
}

/**
 * Check if all required data for the 'drive' mode of transportation is present
 * @param {object} param0 Route data
 * @returns {Boolean} Data validity
 */
function isValidDriveData( { miles, daysPerWeek } ) {
  if (
    miles && isNumber( miles ) &&
    daysPerWeek && isNumber( daysPerWeek )
  ) {
    return true;
  }

  return false;
}

/**
 * Validate all data for a route
 * @param {object} data The transportation tool form data
 * @returns {Boolean} Data validity
 */
function validate( data ) {
  let valid = true;

  valid = isRequiredValid( data );

  if ( !valid ) {
    return valid;
  }

  if ( data.transportation === 'Drive' ) {
    valid = isValidDriveData( data );
  }

  return valid;
}

export default validate;
