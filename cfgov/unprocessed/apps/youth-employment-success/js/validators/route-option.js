import { PLAN_TYPES } from '../data-types/todo-items';

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
 * Determine is a value can be considered empty. It is empty if the value is:
 *
 * null
 * undefined
 * an empty string
 * an empty array
 * an empty object
 *
 * @param {*} value The value to be checked
 * @returns {Boolean} If this value is empty or not
 */
function isEmpty( value ) {
  if ( typeof value === 'undefined' ) {
    return true;
  }

  if ( value === '' ) {
    return true;
  }

  if ( value === null ) {
    return true;
  }

  return false;
}

/**
 * Determine if a field has a value OR is in the user's todo list of actions.
 * Fields in the to-do list do not require values.
 *
 * @param {string} fieldName The name of the field to validate
 * @param {*} value The value of the field being validated
 * @param {array} actionItems List of items the user has in their to-do list of actions
 * @returns {Boolean} Whether or not the field is valid
 */
function valueOrActionPlan( fieldName, value, actionItems ) {
  if (
    !isFieldInActionPlan( fieldName, actionItems ) &&
    isEmpty( value )
  ) {
    return false;
  }

  return true;
}

/**
 * Check if all required fields are present
 * @param {object} data The route option form data
 * @returns {Boolean} Data validity
 */
function isRequiredValid( data ) {
  const todoList = data.actionPlanItems;
  let isValid;

  for ( let i = 0; i < requiredFields.length; i++ ) {
    const fieldName = requiredFields[i];
    // does the data object contain the required field
    if ( data.hasOwnProperty( fieldName ) ) {
      // check if the value exists
      isValid = valueOrActionPlan(
        fieldName,
        data[fieldName],
        todoList
      );
    }

    if ( !isValid ) {
      return false;
    }
  }

  return isValid;
}

/**
 * Check if all required data for the 'drive' mode of transportation is present
 * @param {object} param0 Route data
 * @returns {Boolean} Data validity
 */
function isValidDriveData( { miles, daysPerWeek, actionPlanItems } ) {
  if (
    valueOrActionPlan( 'miles', miles, actionPlanItems ) &&
    valueOrActionPlan( 'daysPerWeek', daysPerWeek, actionPlanItems )
  ) {
    return true;
  }

  return false;
}

/**
 * Determine if a transportation mode that requires entering the averageCost
 * and its associated fields (all modes except 'Drive') is valid
 * @param {Object} data The data to validate
 * @param {String} daysPerWeek The number of days the user will make the trip
 * @param {String} averageCost The cost of the trip
 * @param {Boolean} isMonthlyCost Whether or not the average cost is per day or per month
 * @param {Array} actionPlanItems The current to-do list of trip unknowns
 * @returns {Boolean} Validity of the supplied data
 */
function isValidAverageCost( { daysPerWeek, averageCost, isMonthlyCost, actionPlanItems } ) {
  if (
    isEmpty( averageCost ) ||
    isEmpty( isMonthlyCost )
  ) {
    return false;
  }

  if (
    !isMonthlyCost &&
    !valueOrActionPlan( 'daysPerWeek', daysPerWeek, actionPlanItems )
  ) {
    return false;
  }

  return true;
}

/**
 * Helper function to determine what type of transportation data we should be
 * validating (e.g. 'Drive' vs any other mode of transportation).
 * @param {Object} data The route data to be validated
 * @returns {Boolean} Validity of the supplied data
 */
function isValidTransportationData( data ) {
  let valid = true;

  if ( data.transportation === 'Drive' ) {
    valid = isValidDriveData( data );
  } else {
    valid = isValidAverageCost( data );
  }

  return valid;
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

  valid = isValidTransportationData( data );

  return valid;
}

export default validate;
