const transportation = Object.freeze( {
  WALK: 'Walk',
  DRIVE: 'Drive',
  BIKE: 'Bike',
  PUBLIC_TRANSIT: 'Public transportation',
  DROPPED_OFF: 'Get dropped off'
} );

const transportationMap = Object.freeze( {
  'Walk': 'walking',
  'Drive': 'driving',
  'Bike': 'biking',
  'Public transit': 'public transit',
  'Get droppped off': 'getting dropped off'
} );

export { transportation };
export default transportationMap;
