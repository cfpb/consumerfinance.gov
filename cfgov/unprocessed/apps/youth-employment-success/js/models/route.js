import { assign } from '../util';

/**
 * Factory function for creating a route object. Designed to be used in conjunction
 * with the routeOptionReducer
 * @param {object} [route] object describing the values of the route object
 * @returns {object} a new route object
 */
function createRoute( route = {} ) {
  return assign( {}, {
    transportation: '',
    daysPerWeek: '',
    miles: '',
    averageCost: '',
    isMonthlyCost: null,
    transitTimeHours: '',
    transitTimeMinutes: '',
    actionPlanItems: []
  }, route );
}

export default createRoute;
