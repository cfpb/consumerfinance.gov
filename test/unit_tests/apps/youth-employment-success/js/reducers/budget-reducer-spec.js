import budgetReducer, {
  initialState,
  updateEarnedAction,
  updateSpentAction
} from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/reducers/budget-reducer';
import { UNDEFINED } from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/util';

describe( 'budgetReducer', () => {

  it( 'returns an initial state when it ' +
      'receives an unsupported action type', () => {
    const state = budgetReducer( UNDEFINED, { type: null } );

    expect( state ).toEqual( initialState );
  } );

  it( 'reduces the UPDATE_EARNED action', () => {
    const state = budgetReducer( UNDEFINED, updateEarnedAction( '10' ) );

    expect( state.earned ).toBe( '10' );
    expect( state.spent ).toBe( '' );
  } );

  it( 'reducers the UPDATE_SPENT action', () => {
    const state = budgetReducer( UNDEFINED, updateSpentAction( '10' ) );

    expect( state.spent ).toBe( '10' );
    expect( state.earned ).toBe( '' );
  } );
} );
