import choiceReducer, {
  updateRouteChoiceAction
} from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/reducers/choice-reducer';

let UNDEFINED;

describe( 'choiceReducer', () => {
  it( 'returns an initial state when it receives an unsupported action type', () => {
    const state = choiceReducer( UNDEFINED, { type: null } );

    expect( state ).toEqual( '' );
  } );

  it( 'reduces the .updateRouteChoiceAction', () => {
    const selectedRouteIndex = '1';
    const state = choiceReducer(
      UNDEFINED, updateRouteChoiceAction( selectedRouteIndex )
    );

    expect( state ).toBe( selectedRouteIndex );
  } );
} );
