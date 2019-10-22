const TRANSPORTATION = Object.freeze( {
  WALK: 'Walk',
  DRIVE: 'Drive',
  BIKE: 'Bike',
  PUBLIC_TRANSIT: 'Public transportation',
  DROPPED_OFF: 'Get dropped off',
  RIDESHARE: 'Rideshare or cab'
} );

const transportationMap = Object.freeze( {
  [TRANSPORTATION.WALK]: 'walking',
  [TRANSPORTATION.DRIVE]: 'driving',
  [TRANSPORTATION.BIKE]: 'biking',
  [TRANSPORTATION.PUBLIC_TRANSIT]: 'public transit',
  [TRANSPORTATION.DROPPED_OFF]: 'getting dropped off',
  [TRANSPORTATION.RIDESHARE]: 'rideshare or cab'
} );

export { TRANSPORTATION };
export default transportationMap;
