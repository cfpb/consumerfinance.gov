import routeOptionReducer, {
  initialState,
  updateDailyCostAction,
  updateDaysPerWeekAction,
  updateMilesAction,
  updateTransportationAction
} from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/reducers/route-option-reducer';
import { UNDEFINED } from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/util';

// Arbitrary value to ensure reducer is updating properly
const nextValue = '15';

describe( 'routeOptionReducer', () => {
  it( 'returns an initial state when it recevives an unsupported action type', () => {
    const state = routeOptionReducer( UNDEFINED, { type: null } );

    expect( state ).toEqual( initialState );
  } );

  it( 'reduces .updateDailyCostAction', () => {
    const state = routeOptionReducer(
      UNDEFINED,
      updateDailyCostAction( nextValue )
    );
    const { dailyCost, ...rest } = state;

    expect( dailyCost ).toBe( nextValue );
    Object.entries( rest ).forEach( ( [ key, value ] ) => expect( value ).toBe( initialState[key] )
    );
  } );

  it( 'reduces .updateDaysPerWeekAction', () => {
    const state = routeOptionReducer(
      UNDEFINED,
      updateDaysPerWeekAction( nextValue )
    );
    const { daysPerWeek, ...rest } = state;

    expect( daysPerWeek ).toBe( nextValue );
    Object.entries( rest ).forEach( ( [ key, value ] ) => expect( value ).toBe( initialState[key] )
    );
  } );

  it( 'reduces .updateMilesAction', () => {
    const state = routeOptionReducer(
      UNDEFINED,
      updateMilesAction( nextValue )
    );
    const { miles, ...rest } = state;
    expect( miles ).toBe( nextValue );
    Object.entries( rest ).forEach( ( [ key, value ] ) => expect( value ).toBe( initialState[key] )
    );
  } );

  it( 'reduces .updateTransportation', () => {
    let state = routeOptionReducer(
      initialState,
      updateTransportationAction( 'Walk' )
    );

    expect( state.transportation ).toBe( 'Walk' );

    state = routeOptionReducer(
      state,
      updateTransportationAction( 'Drive' )
    );

    expect( state.transportation ).toBe( 'Drive' );
  } );
} );
