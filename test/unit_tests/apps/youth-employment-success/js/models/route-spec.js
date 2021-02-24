import
createRoute
  from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/models/route';

describe( 'route factory function', () => {
  it( 'constructs a route object', () => {
    const newRoute = createRoute();

    [ 'transportation', 'daysPerWeek', 'miles', 'averageCost' ]
      .forEach( prop => {
        expect( newRoute[prop] ).toBeDefined();
      } );
  } );

  it( 'constructs a route object with supplied data', () => {
    const props = { transportation: 'Drive', miles: '20' };
    const newRoute = createRoute( props );

    expect( newRoute.transportation ).toBe( props.transportation );
    expect( newRoute.miles ).toBe( props.miles );
    expect( newRoute.daysPerWeek ).toBe( '' );
    expect( newRoute.averageCost ).toBe( '' );
  } );
} );
